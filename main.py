import argparse
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os
from supabase.client import Client, create_client
from langchain_openai import OpenAIEmbeddings
from ingest_pipeline.update_docs_rag import ingest_data, load_sitemap, load_recursive_url
from ingest_pipeline.constants import SITEMAP_URLS
from typing import List
import asyncio


load_dotenv()

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")


async def main_async(names: List[str], only_other: bool = False, only_sitemap: bool = True, clean_ingest: bool = False):

    # Load documents async and ingest them into the vector store
    raw_documents = []

    # Figure out whether to ingest to blue or green table
    table_suffix_response = supabase.table('ingestion_metadata').select("*").eq("active", False).execute()

    table_suffix = table_suffix_response.data[0].get("environment")

    print(f"Ingesting into {table_suffix} ")

    executor = ThreadPoolExecutor(max_workers=10)

    for sitemap in [sitemap for sitemap in SITEMAP_URLS if sitemap["table_name"] in names]:
        # Drop the table
        if clean_ingest:
            supabase.table(f"{sitemap['table_name']}_{table_suffix}").delete().neq("content", "null").execute()

        if only_sitemap:
            raw_documents.append(executor.submit(load_sitemap, sitemap))
        elif only_other:
            raw_documents.append(executor.submit(load_recursive_url, sitemap))
        else:
            raw_documents.append(executor.submit(load_sitemap, sitemap))
            raw_documents.append(executor.submit(load_recursive_url, sitemap))

    docs_to_ingest = [future.result() for future in raw_documents]

    ingest_futures = []

    for doc in docs_to_ingest:
        asyncio.create_task(ingest_data(data=doc, table_suffix=table_suffix))

    await asyncio.gather(*ingest_futures)

    # At the end of the ingestion process, update the ingestion_metadata
    table_update_response = supabase.table('ingestion_metadata').update({
        "active": True,
        "updated_at": "now()"
    }).eq("environment", table_suffix).execute()

    # Update the other row to active: False
    other_row = "green" if table_suffix == "blue" else "blue"

    other_table_update_response = supabase.table('ingestion_metadata').update({
        "active": False
    }).eq("environment", other_row).execute()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Embed documents from various sources."
    )

    parser.add_argument("--names", nargs="*", help="Specify a list of the tables to ingest, e.g. vscode_documents")
    parser.add_argument("--only-sitemap", action="store_true", help="Only ingest the main urls from the specified tables")
    parser.add_argument("--only-other", action="store_true", help="Only ingest the other_urls from the specified tables")
    parser.add_argument("--clean", action="store_true", help="Clean the table before ingesting")

    is_main = True

    while is_main:
        args = parser.parse_args()
        
        asyncio.run(main_async(names=args.names, only_other=args.only_other, only_sitemap=args.only_sitemap, clean_ingest=args.clean))

        is_main = False
