from langchain.document_loaders.sitemap import SitemapLoader

# fixes a bug with asyncio and jupyter
import nest_asyncio

nest_asyncio.apply()