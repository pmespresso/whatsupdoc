from pydantic import BaseModel
from typing import List, Any


class SitemapLoaderConfig(BaseModel):
    web_path: str
    filter_urls: List[str]
    table_name: str


class DocumentData(BaseModel):
    docs: List[str]
    table_name: str
