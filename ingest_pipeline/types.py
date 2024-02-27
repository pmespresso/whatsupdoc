from pydantic import BaseModel
from typing import List, Any
from langchain.schema import Document


class SitemapLoaderConfig(BaseModel):
    web_path: str
    filter_urls: List[str]
    other_urls: List[str]
    is_local: bool
    table_name: str


class DocumentData(BaseModel):
    docs: List[Document]
    table_name: str
