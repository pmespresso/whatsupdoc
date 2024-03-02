from pydantic import BaseModel
from typing import List, Any, Optional
from langchain.schema import Document


class LoaderConfig(BaseModel):
    display_name: str
    documents_table_name: str
    documentation_url: str
    github_discussion_url: Optional[str]
    logo_url: Optional[str]
    sitemap_url: Optional[str]
    sitemap_filter_urls: Optional[List[str]]
    other_urls: Optional[List[str]]


class DocumentData(BaseModel):
    docs: List[Document]
    table_name: str
