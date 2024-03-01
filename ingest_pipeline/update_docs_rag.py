from bs4 import BeautifulSoup as Soup, SoupStrainer
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.supabase import SupabaseVectorStore
from langchain.utils.html import PREFIXES_TO_IGNORE_REGEX, SUFFIXES_TO_IGNORE_REGEX
from langchain.document_loaders.sitemap import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_experimental.text_splitter import SemanticChunker

import os
import re
from supabase.lib.client_options import ClientOptions
from supabase.client import Client, create_client

from .types import SitemapLoaderConfig, DocumentData
from .util import tiktoken_len

load_dotenv()

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
client_options = ClientOptions(postgrest_client_timeout=None)
supabase: Client = create_client(supabase_url=supabase_url, supabase_key=supabase_key, options=client_options)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=200,
#     length_function=tiktoken_len,
#     separators=["\n" * i for i in range(0, 43 + 1)] + [" ", ""],
# )
text_splitter = SemanticChunker(embeddings=embeddings)



def metadata_extractor(meta: dict, soup: Soup) -> dict:
    title = soup.find("title")
    description = soup.find("meta", attrs={"name": "description"})
    html = soup.find("html")
    return {
        "source": meta["loc"],
        "title": title.get_text() if title else "",
        "description": description.get("content", "") if description else "",
        "language": html.get("lang", "") if html else "",
        **meta,
    }

def load_sitemap(loaderConfig: SitemapLoaderConfig):
    sitemaploader = SitemapLoader(
        web_path=loaderConfig['web_path'],
        filter_urls=loaderConfig['filter_urls'],
        is_local=loaderConfig['is_local'],
         bs_kwargs={
            "parse_only": SoupStrainer(
                name=("article")
            ),
        },
        meta_function=metadata_extractor,
        continue_on_failure=True
    )

    docs = sitemaploader.load_and_split(text_splitter=text_splitter)

    print(f"Loaded {len(docs)}, e.g. {docs[0]}")

    table_name = loaderConfig['table_name']

    return DocumentData(docs=docs, table_name=table_name)

def simple_extractor(html: str) -> str:
    soup = Soup(html, "lxml", parse_only=SoupStrainer(name=("article", "main", "title", "content", "markdown")))
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()

def load_recursive_url(loaderConfig: SitemapLoaderConfig):
    docs = []

    # check if loaderConfig has a key other_urls
    if 'other_urls' not in loaderConfig:
        print("No other_urls in loaderConfig")
        return

    for url in loaderConfig['other_urls']:
        print(f"Loading additional documents from {url}")
        recursive_url_loader = RecursiveUrlLoader(
            url=url, 
            max_depth=8,
            extractor=simple_extractor,
            prevent_outside=True,
            use_async=True,
            timeout=600,
            # Drop trailing / to avoid duplicate pages.
            link_regex=(
                f"href=[\"']{PREFIXES_TO_IGNORE_REGEX}((?:{SUFFIXES_TO_IGNORE_REGEX}.)*?)"
                r"(?:[\#'\"]|\/[\#'\"])"
            ),
            check_response_status=True,
            exclude_dirs=(
                "https://python.langchain.com/docs/additional_resources/",
                "https://api.python.langchain.com/en/latest/_sources",
                "https://api.python.langchain.com/en/latest/_modules",
            )
        ).load()

        print("Loaded.")

        documents = text_splitter.split_documents(recursive_url_loader)

        print("Split.")

        docs = [*docs, *documents]
        
        print("length of docs", len(docs))

        table_name = loaderConfig['table_name']
        print("table_name", table_name)
    result =  DocumentData(docs=docs, table_name=table_name)
    print("result", result)
    return result

async def ingest_data(data: DocumentData):

    print(f"Ingesting {len(data.docs)} documents into {data.table_name}. ")

    vectorstore = SupabaseVectorStore.from_documents(
        client=supabase,
        embedding=embeddings,
        table_name=data.table_name,
        documents=data.docs,
        query_name=f"match_{data.table_name}"
    )

    # set the updated_at column to the current time
    supabase.table('knowledgebases').update({"updated_at": "now()"}).eq("documents_table_name", data.table_name).execute()

    updated_at_response = supabase.table('knowledgebases').select("updated_at").eq("documents_table_name", data.table_name).execute()

    updated_at = updated_at_response.data[0].get("updated_at")

    print(f"Ingestion complete at {updated_at}")

    return vectorstore