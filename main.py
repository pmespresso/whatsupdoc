from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os
from supabase.client import Client, create_client
from langchain.vectorstores.supabase import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from ingest_pipeline.update_docs_rag import load_docs, ingest_data
from ingest_pipeline.constants import SITEMAP_URLS
import asyncio

load_dotenv()

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")


async def main_async():
    # Load documents async and ingest them into the vector store
    raw_documents = []

    executor = ThreadPoolExecutor(max_workers=10)

    for sitemap in SITEMAP_URLS:
        raw_documents.append(executor.submit(load_docs, sitemap))

    docs_to_ingest = [future.result() for future in raw_documents]

    ingest_futures = []

    for doc in docs_to_ingest:
        ingest_futures.append(asyncio.create_task(ingest_data(doc)))

    await asyncio.gather(*ingest_futures)

    print("Ingestion complete")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()