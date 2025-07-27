import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Import and apply custom headers for all requests
from request_headers import DEFAULT_REQUEST_HEADERS


# Logging configuration
LOG_FILE = os.environ.get('LOG_FILE', 'response.log')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# Scrapy bot and modules
BOT_NAME = 'imdb_scraper'
SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'



# robots.txt rules
ROBOTSTXT_OBEY = True

# Only allow the main request, do not follow links or download additional resources
DEPTH_LIMIT = 0
DOWNLOAD_HANDLERS = {
    'http': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
    'https': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
}
MEDIA_ALLOW_REDIRECTS = False


# --- ROTATING PROXIES AND RETRY ---
# Enable retry and configure retry/backoff settings
RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]
RETRY_BACKOFF_BASE = 1
RETRY_BACKOFF_MAX = 60

# Enable/disable rotating proxy from .env
USE_PROXY = os.getenv('USE_PROXY', 'true').lower() == 'true'
print(f"USE_PROXY: {os.getenv('USE_PROXY', 'true')}")

if USE_PROXY:
    # List of proxies to rotate (public and local)
    ROTATING_PROXY_LIST = [
        'http://51.158.68.68:8811',
        'http://185.199.228.140:7300',
        'http://127.0.0.1:8080'
    ]
    # Enable rotating proxy and ban detection middlewares
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 120,
        'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
        'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    }
else:
    # Use default middlewares without proxy rotation
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 120,
    }


# Enable the PostgreSQL pipeline for saving items
ITEM_PIPELINES = {
    'pipelines.pipelines_movie_actor.PostgresMovieActorPipeline': 300,
}
