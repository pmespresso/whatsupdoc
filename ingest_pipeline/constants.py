from typing import List, Any
from .types import SitemapLoaderConfig

SITEMAP_URLS: List[SitemapLoaderConfig] = [
    {
        "web_path": "https://nextjs.org/sitemap.xml",
        "filter_urls":["^https:\/\/nextjs\.org\/docs"],
        "table_name": "nextjs_docs"
    },
    {
        "web_path": "https://stripe.com/sitemap/partition-2.xml",
        "filter_urls":["^https:\/\/stripe\.com\/docs"],
        "table_name": "stripe_docs"
    },
]