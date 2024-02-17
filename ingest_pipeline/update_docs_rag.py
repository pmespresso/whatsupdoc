from pydantic import BaseModel
from typing import List, Any
from langchain.document_loaders.sitemap import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from supabase.client import Client, create_client
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.supabase import SupabaseVectorStore
import os
from dotenv import load_dotenv
from tqdm import tqdm
from supabase.lib.client_options import ClientOptions

from .types import SitemapLoaderConfig, DocumentData
from .util import tiktoken_len, get_ids, chunks

load_dotenv()

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
client_options = ClientOptions(postgrest_client_timeout=None)
supabase: Client = create_client(supabase_url=supabase_url, supabase_key=supabase_key, options=client_options)

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

def load_docs(loaderConfig: SitemapLoaderConfig):
    # check the last time it was updated in the knowledgebases table, and only ingest if it's been more than 28 days
    # is_it_a_row_to_update = supabase.table('knowledgebases').select("updated_at").eq("documents_table_name", loaderConfig['table_name']).gte("updated_at", "now() - interval '1 days'").execute()

    # if is_it_a_row_to_update.data:
    #     print(f"Skipping {loaderConfig['table_name']}, it was updated in the last 28 days")
    #     return

    sitemaploader = SitemapLoader(
        web_path=loaderConfig['web_path'],
        filter_urls=loaderConfig['filter_urls'],
        is_local=loaderConfig['is_local'],
        continue_on_failure=True
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=tiktoken_len,
        separators=["\n" * i for i in range(0, 43 + 1)] + [" ", ""],
    )

    docs = sitemaploader.load_and_split(text_splitter=text_splitter)
    table_name = loaderConfig['table_name']

    return DocumentData(docs=docs, table_name=table_name)

async def ingest_data(data: DocumentData, table_suffix: str = "blue"):
    print("Ingesting into", table_suffix)

    print(f"Ingesting {len(data.docs)} documents into {data.table_name}. ")

    vectorstore = SupabaseVectorStore.from_documents(
        client=supabase,
        embedding=embeddings,
        table_name=f"{data.table_name}_{table_suffix}",
        documents=data.docs,
        query_name=f"match_{data.table_name}_{table_suffix}",
        chunk_size=500
    )

    # set the updated_at column to the current time
    supabase.table('knowledgebases').update({"updated_at": "now()"}).eq("documents_table_name", data.table_name).execute()

    updated_at_response = supabase.table('knowledgebases').select("updated_at").eq("documents_table_name", data.table_name).execute()

    updated_at = updated_at_response.data[0].get("updated_at")

    print(f"Ingestion complete at {updated_at}")

    return vectorstore