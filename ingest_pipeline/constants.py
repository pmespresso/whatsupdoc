from typing import List, Any
from .types import SitemapLoaderConfig

SITEMAP_URLS: List[SitemapLoaderConfig] = [
    {
        "web_path": "https://code.visualstudio.com/sitemap.xml",
        "filter_urls":["^https:\/\/code\.visualstudio\.com\/api"],
        "table_name": "vscode_documents",
        "is_local": False
    },
    # {
    #     "web_path": "https://nextjs.org/sitemap.xml",
    #     "filter_urls":["^https:\/\/nextjs\.org\/docs", "^https:\/\/nextjs\.org\/blogs"],
    #     "table_name": "nextjs_documents",
    #     "is_local": False
    # },
    # {
    #     "web_path": "./langchainjs-sitemap.xml",
    #     "table_name": "langchainjs_documents",
    #     "filter_urls": [],
    #     "is_local": True
    # },
    # {
    #     "web_path": "https://stripe.com/sitemap/partition-2.xml",
    #     "filter_urls":["^https:\/\/stripe\.com\/docs"],
    #     "table_name": "stripe_documents",
    #     "is_local": False
    # },
    # {
    #     "web_path": "https://stripe.com/sitemap/partition-1.xml",
    #     "filter_urls":["^https:\/\/stripe\.com\/docs"],
    #     "table_name": "stripe_documents",
    #     "is_local": False
    # },
    # {
    #     "web_path": "https://developer.paddle.com/sitemap.xml",
    #     "filter_urls":[],
    #     "table_name": "paddle_documents",
    #     "is_local": False
    # }
]