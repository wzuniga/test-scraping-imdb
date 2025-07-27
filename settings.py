import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

 # Logging configuration from .env
LOG_FILE = os.environ.get('LOG_FILE', 'response.log')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

BOT_NAME = 'imdb_scraper'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'


ROBOTSTXT_OBEY = True

 # Only allow the main request, do not follow links or download additional resources
DEPTH_LIMIT = 0
DOWNLOAD_HANDLERS = {
    'http': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
    'https': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
}
MEDIA_ALLOW_REDIRECTS = False


 # Import and apply custom headers for all requests
from request_headers import DEFAULT_REQUEST_HEADERS



 # --- ROTATING PROXIES AND RETRY ---
RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]
RETRY_BACKOFF_BASE = 1
RETRY_BACKOFF_MAX = 60

 # Enable/disable rotating proxy from .env
USE_PROXY = os.getenv('USE_PROXY', 'true').lower() == 'true'
print(f"USE_PROXY: {os.getenv('USE_PROXY', 'true')}")

if USE_PROXY:
    ROTATING_PROXY_LIST = [
        'http://51.158.68.68:8811',
        'http://185.199.228.140:7300',
        'http://85.193.191.199:8080',
        'http://127.0.0.1:8080'
    ]
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 120,
        'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
        'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    }
else:
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 120,
    }

 # Enable the PostgreSQL pipeline
ITEM_PIPELINES = {
    'pipelines.pipelines_movie_actor.PostgresMovieActorPipeline': 300,
}
