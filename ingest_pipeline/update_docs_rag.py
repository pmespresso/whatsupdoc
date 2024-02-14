from pydantic import BaseModel
from typing import List, Any
from langchain.document_loaders.sitemap import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from supabase.client import Client, create_client
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.supabase import SupabaseVectorStore
import os
from dotenv import load_dotenv
from tqdm.asyncio import tqdm as tqdm_asyncio

from .types import SitemapLoaderConfig, DocumentData
from .util import tiktoken_len

load_dotenv()


def load_docs(loaderConfig: SitemapLoaderConfig):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=tiktoken_len,
        separators=["\n" * i for i in range(0, 43 + 1)] + [" ", ""],
    )
    sitemaploader = SitemapLoader(
        web_path=loaderConfig['web_path'],
        filter_urls=loaderConfig['filter_urls'],
    )

    docs = sitemaploader.load_and_split(text_splitter=text_splitter)
    table_name = sitemaploader['table_name']

    return DocumentData(docs=docs, table_name=table_name)

async def ingest_data(data: DocumentData):
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
    supabase: Client = create_client(supabase_url, supabase_key)

    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

    vector_store = SupabaseVectorStore(
        client=supabase,
        table_name=data.table_name,
        embedding=embeddings,
        query_name=f"match_{data.table_name}",
        chunk_size=500
    )

    # vector_store = await SupabaseVectorStore.from_documents(
    #     documents=data.docs,
    #     embedding=embeddings,
    #     client=supabase,
    #     table_name=data.table_name,
    #     query_name=f"match_{data.table_name}",
    #     chunk_size=500
    # )

    print(f"Vector store created for {vector_store.table_name}") 


