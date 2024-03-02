import argparse
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os
from supabase.client import Client, create_client
from langchain_openai import OpenAIEmbeddings
from ingest_pipeline.update_docs_rag import ingest_data, load_sitemap, load_github_discussions, load_other_urls, load_documentation_url
from ingest_pipeline.constants import LOADER_CONFIGS
from typing import List
from ingest_pipeline.types import LoaderConfig
import asyncio


load_dotenv()

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# FIXME
def create_table_with_embedding(table_name: str):
    print(f"Creating table {table_name} with embedding")
    # SQL command to create a table
    sql_command = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id uuid primary key,
        content text,
        metadata jsonb,
        embedding vector(3072) -- Adjust this type according to your actual requirements
    );
    """
    
    # Execute the SQL command
    data = supabase.table(table_name).execute_sql(sql_command)
    print(f"Table {table_name} created or already exists.")

def create_knowledgebase_entry(loaderConfig: LoaderConfig):
    print(f"Creating knowledgebase entry for {loaderConfig}")
    
    supabase.table("knowledgebases").insert(
        {
            "name": loaderConfig['display_name'],
            "documents_table_name": loaderConfig['documents_table_name'],
            "documentation_url": loaderConfig['documentation_url'],
            "github_discussions_url": loaderConfig['github_discussions_url'],
            "logo_url": loaderConfig['logo_url'],
            "sitemap_url": loaderConfig['sitemap_url'],
            "sitemap_filter_urls": loaderConfig['sitemap_filter_urls'],
            "other_links": loaderConfig['other_urls']
        }).execute()

async def main_async(names: List[str], only_other: bool = False, only_docs: bool = False, only_github: bool=False, only_sitemap: bool = True, clean_ingest: bool = False):

    # Load documents async and ingest them into the vector store
    raw_documents = []

    executor = ThreadPoolExecutor(max_workers=10)

    for loaderConfig in [loaderConfig for loaderConfig in LOADER_CONFIGS if loaderConfig['documents_table_name'] in names]:
        create_knowledgebase_entry(loaderConfig)

        # Delete all records if clean_ingest is True
        if clean_ingest:
            # delete this row where content is not null
            print(f"Cleaning table {loaderConfig['documents_table_name']}")
            supabase.table(loaderConfig['documents_table_name']).delete().neq("content", "null").execute()
        

        if only_sitemap:
            raw_documents.append(executor.submit(load_sitemap, loaderConfig))
        elif only_other:
            raw_documents.append(executor.submit(load_other_urls, loaderConfig))
        elif only_github:
            raw_documents.append(executor.submit(load_github_discussions, loaderConfig))
        elif only_docs:
            raw_documents.append(executor.submit(load_documentation_url, loaderConfig))
        else:
            # Load everything from everywhere
            raw_documents.append(executor.submit(load_documentation_url, loaderConfig))
            raw_documents.append(executor.submit(load_sitemap, loaderConfig))
            raw_documents.append(executor.submit(load_github_discussions, loaderConfig))
            raw_documents.append(executor.submit(load_other_urls, loaderConfig))

    docs_to_ingest = [future.result() for future in raw_documents]

    ingest_futures = []

    for doc in docs_to_ingest:
        asyncio.create_task(ingest_data(data=doc))

    await asyncio.gather(*ingest_futures)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Embed documents from various sources."
    )

    parser.add_argument("--names", nargs="*", help="Specify a list of the tables to ingest, e.g. vscode_documents")
    parser.add_argument("--only-sitemap", action="store_true", help="Only ingest the main urls from the specified tables")
    parser.add_argument("--only-docs", action="store_true", help="Only ingest the documentation from the specified tables")
    parser.add_argument("--only-github", action="store_true", help="Only ingest the Github discussion url from the specified tables")
    parser.add_argument("--only-other", action="store_true", help="Only ingest the other_urls from the specified tables")
    parser.add_argument("--clean", action="store_true", help="Clean the table before ingesting")

    is_main = True

    while is_main:
        args = parser.parse_args()
        
        asyncio.run(main_async(names=args.names, only_other=args.only_other, only_docs=args.only_docs, only_github=args.only_github, only_sitemap=args.only_sitemap, clean_ingest=args.clean))

        is_main = False
