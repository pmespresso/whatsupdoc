from typing import List, Any
from .types import SitemapLoaderConfig

SITEMAP_URLS: List[SitemapLoaderConfig] = [
    {
        "web_path": "https://code.visualstudio.com/sitemap.xml",
        "filter_urls":["^https:\/\/code\.visualstudio\.com\/api", "^https:\/\/code\.visualstudio\.com\/api/extension-guides"],
        "table_name": "vscode_documents",
        "is_local": False
    },
    {
        "web_path": "https://nextjs.org/sitemap.xml",
        "filter_urls":["^https:\/\/nextjs\.org\/docs", "^https:\/\/nextjs\.org\/blogs"],
        "table_name": "nextjs_documents",
        "is_local": False
    },
    {
        "web_path": "https://js.langchain.com/sitemap.xml",
        "table_name": "langchainjs_documents",
        "other_urls": ["https://www.pinecone.io/learn/series/langchain/langchain-expression-language/", "https://js.langchain.com/docs/guides"],
        "filter_urls": ["^https:\/\/js\.langchain\.com\/docs\/modules", "^https:\/\/js\.langchain\.com\/docs\/get_started", "^https:\/\/js\.langchain\.com\/docs\/expression_language", "^https:\/\/js\.langchain\.com\/docs\/security"],
        "is_local": False
    },
    {
        "web_path": "https://python.langchain.com/sitemap.xml",
        "filter_urls":["^https:\/\/python\.langchain\.com\/docs\/modules", "^https:\/\/python\.langchain\.com\/docs\/get_started", "^https:\/\/python\.langchain\.com\/cookbook", "^https:\/\/python\.langchain\.com\/api"],
        "other_urls": ["https://www.pinecone.io/learn/series/langchain/langchain-expression-language/", "https://github.com/langchain-ai/langchain/discussions", "https://python.langchain.com/docs"],
        "table_name": "langchain_documents",
        "is_local": False
    },
    {
        "web_path": "https://stripe.com/sitemap/partition-2.xml",
        "filter_urls":["^https:\/\/stripe\.com\/docs"],
        "table_name": "stripe_documents",
        "is_local": False
    },
    {
        "web_path": "https://stripe.com/sitemap/partition-1.xml",
        "filter_urls":["^https:\/\/stripe\.com\/docs"],
        "table_name": "stripe_documents",
        "is_local": False
    },
    {
        "web_path": "https://developer.paddle.com/sitemap.xml",
        "filter_urls":[],
        "table_name": "paddle_documents",
        "is_local": False
    }
]