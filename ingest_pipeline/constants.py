from typing import List, Any
from .types import LoaderConfig

# Github Discussions Sort
# ?discussions_q=sort%3Atop+created%3A>%3D2023-03-02+is%3Aanswered

LOADER_CONFIGS: List[LoaderConfig] = [
    {
        "display_name": "Substrate",
        "documents_table_name": "substrate_documents",
        "documentation_url": "",
        "github_discussions_url": "",
        "logo_url": "https://substrate.dev/img/substrate-logo.svg",
        "sitemap_url": "https://docs.substrate.io/sitemap.xml",
        "sitemap_filter_urls": [],
        "other_urls": []
    },
    {
        "display_name": "Polkadot",
        "documents_table_name": "polkadot_documents",
        "documentation_url": "https://docs.substrate.io/learn/xcm-communication/",
        "github_discussions_url": "",
        "logo_url": "https://wiki.polkadot.network/img/Polkadot_Logo_Horizontal_Pink-Black.svg",   
        "sitemap_url": "https://wiki.polkadot.network/sitemap.xml",
        "sitemap_filter_urls":["^https:\/\/wiki\.polkadot\.network\/docs"],
        "other_urls": ["https://forum.polkadot.network/top"]
    },
    {
        "display_name": "Solana",
        "documents_table_name": "solana_documents",
        "documentation_url": "https://solana.com/docs",
        "github_discussions_url": None,
        "logo_url": None,
        "sitemap_url": "https://solana.com/sitemap-0.xml",
        "sitemap_filter_urls": ["^https://solana.com/docs"],
        "other_urls": ["https://docs.solanalabs.com/", "https://solana.com/docs", "https://solana.com/news"]
    },
    {
        "display_name": "Visual Studio Code",
        "documents_table_name": "vscode_documents",
        "documentation_url": "https://code.visualstudio.com/api",
        "github_discussions_url": None,
        "logo_url": None,
        "sitemap_url": "https://code.visualstudio.com/sitemap.xml",
        "sitemap_filter_urls": ["^https://code.visualstudio.com/api", "^https://code.visualstudio.com/api/extension-guides"],
        "other_urls": ["https://code.visualstudio.com/api/references/"]
    },
    {
        "display_name": "Next.js",
        "documents_table_name": "nextjs_documents",
        "documentation_url": "https://nextjs.org/docs",
        "github_discussions_url": None,
        "logo_url": None,
        "sitemap_url": "https://nextjs.org/sitemap.xml",
        "sitemap_filter_urls": ["^https://nextjs.org/docs"],
        "other_urls": ["https://nextjs.org/blog", "https://nextjs.org/docs/app/api-reference", "https://github.com/vercel/next.js/discussions/categories/app-router?discussions_q=is:open+category:\"App Router\"+sort:top"]
    },
    {
        "display_name": "Langchain JS",
        "documents_table_name": "langchainjs_documents",
        "documentation_url": "https://js.langchain.com/docs",
        "github_discussions_url": None,
        "logo_url": None,
        "sitemap_url": "https://js.langchain.com/sitemap.xml",
        "sitemap_filter_urls": ["^https://js.langchain.com/docs/modules", "^https://js.langchain.com/docs/get_started", "^https://js.langchain.com/docs/expression_language", "^https://js.langchain.com/docs/security"],
        "other_urls": ["https://www.pinecone.io/learn/series/langchain/langchain-expression-language/", "https://js.langchain.com/docs/guides"]
    },
    {
        "display_name": "Langchain Python",
        "documents_table_name": "langchain_documents",
        "documentation_url": "https://python.langchain.com/docs",
        "github_discussions_url": "https://github.com/langchain-ai/langchain/discussions",
        "logo_url": None,  # Assuming no logo URL is provided
        "sitemap_url": "https://python.langchain.com/sitemap.xml",
        "sitemap_filter_urls": [
            "^https://python.langchain.com/docs/modules",
            "^https://python.langchain.com/docs/get_started",
            "^https://python.langchain.com/cookbook",
            "^https://python.langchain.com/api"
        ],
        "other_urls": [
            "https://www.pinecone.io/learn/series/langchain/langchain-expression-language/",
            "https://python.langchain.com/docs"
        ]
    },
    {
        "display_name": "Stripe Partition 2",
        "documents_table_name": "stripe_documents",
        "documentation_url": "https://stripe.com/docs",
        "github_discussions_url": None,
        "logo_url": None,  # Assuming no logo URL is provided
        "sitemap_url": "https://stripe.com/sitemap/partition-2.xml",
        "sitemap_filter_urls": ["^https://stripe.com/docs"],
        "other_urls": []  # Assuming no additional URLs
    },
    {
        "display_name": "Stripe Partition 1",
        "documents_table_name": "stripe_documents",
        "documentation_url": "https://stripe.com/docs",
        "github_discussions_url": None,
        "logo_url": None,  # Assuming no logo URL is provided
        "sitemap_url": "https://stripe.com/sitemap/partition-1.xml",
        "sitemap_filter_urls": ["^https://stripe.com/docs"],
        "other_urls": []  # Assuming no additional URLs
    },
    {
        "display_name": "Paddle",
        "documents_table_name": "paddle_documents",
        "documentation_url": "https://developer.paddle.com/",
        "github_discussions_url": None,
        "logo_url": None,  # Assuming no logo URL is provided
        "sitemap_url": "https://developer.paddle.com/sitemap.xml",
        "sitemap_filter_urls": [],  # No filters provided
        "other_urls": []  # Assuming no additional URLs
    }
]