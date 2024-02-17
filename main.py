from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os
from supabase.client import Client, create_client
from langchain_openai import OpenAIEmbeddings
from ingest_pipeline.update_docs_rag import load_docs, ingest_data
from ingest_pipeline.constants import SITEMAP_URLS
from ingest_pipeline.util import get_ids
import asyncio


load_dotenv()

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")


async def main_async():
    # Load documents async and ingest them into the vector store
    raw_documents = []

    # Figure out whether to ingest to blue or green table
    table_suffix_response = supabase.table('ingestion_metadata').select("*").eq("active", False).execute()

    table_suffix = table_suffix_response.data[0].get("environment")

    print(f"Ingesting into {table_suffix} ")

    executor = ThreadPoolExecutor(max_workers=10)

    for sitemap in SITEMAP_URLS:
        raw_documents.append(executor.submit(load_docs, sitemap))

    docs_to_ingest = [future.result() for future in raw_documents]

    ingest_futures = []

    for doc in docs_to_ingest:
        asyncio.create_task(ingest_data(doc, table_suffix=table_suffix))

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


def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()