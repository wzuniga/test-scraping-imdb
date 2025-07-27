import scrapy
import json
from utils.utils import get_imdb_top_url, get_logger
from request_headers import DEFAULT_REQUEST_HEADERS
from utils.imdb_utils import extract_movies_data
from utils.imdb_utils import extract_next_data_json, extract_actor_items
import os
from utils.utils import get_logger


class ImdbActorSpider(scrapy.Spider):
    """
    Scrapy spider to extract actor data from IMDb top movies.
    Handles retries, proxy logging, and parses actor details from movie pages.
    """
    name = 'imdb_actor'

    def __init__(self, *args, **kwargs):
        """Initialize the spider and set up the logger."""
        super().__init__(*args, **kwargs)
        self._logger = get_logger(self.name)

    @property
    def logger(self):
        """Return the custom logger for this spider."""
        return self._logger

    async def start(self):
        """Start crawling from the IMDb top URL or provided URLs."""
        urls = getattr(self, 'start_urls', None) or [get_imdb_top_url()]
        for url in urls:
            self.logger.info(f'Starting crawl for URL: {url}')
            yield scrapy.Request(url, headers=DEFAULT_REQUEST_HEADERS)

    def parse(self, response):
        """Parse the top movies page, extract movie IDs, and request detail pages."""
        # Log proxy info if present
        proxy = response.meta.get('proxy') or response.request.meta.get('proxy')
        if proxy:
            self.logger.info(f'Using proxy: {proxy}')
        else:
            self.logger.info('No proxy (direct connection)')
        retry_times = int(os.environ.get('RETRY_TIMES', 3))
        try:
            next_data_json = extract_next_data_json(response)
        except ValueError as e:
            retry_count = response.meta.get('retry_count', 0)
            if retry_count < retry_times:
                self.logger.warning(f"__NEXT_DATA__ not found, retrying ({retry_count+1}/{retry_times}): {response.url}")
                yield scrapy.Request(
                    url=response.url,
                    callback=self.parse,
                    dont_filter=True,
                    meta={**response.meta, 'retry_count': retry_count+1},
                    headers=DEFAULT_REQUEST_HEADERS
                )
            else:
                self.logger.error(f"Persistent failure: {e}")
            return
        movies_ids = extract_movies_data(next_data_json)
        self.logger.info(f'Total movies found: {len(movies_ids)}')
        for movie_id in movies_ids[:50]:
            detail_url = f'https://www.imdb.com/es-es/title/{movie_id}'
            self.logger.info(f'Requesting detail page for movie_id: {movie_id}')
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_movie_detail,
                meta={'movie_id': movie_id},
                headers=DEFAULT_REQUEST_HEADERS
            )

    def parse_movie_detail(self, response):
        """Parse the movie detail page and yield actor items."""
        # Log proxy info if present
        proxy = response.meta.get('proxy') or response.request.meta.get('proxy')
        if proxy:
            self.logger.info(f'Using proxy: {proxy}')
        else:
            self.logger.info('No proxy (direct connection)')
        retry_times = int(os.environ.get('RETRY_TIMES', 3))
        movie_id = response.meta['movie_id']
        try:
            next_data_json = extract_next_data_json(response, detail=True, movie_id=movie_id)
        except ValueError as e:
            retry_count = response.meta.get('retry_count', 0)
            if retry_count < retry_times:
                self.logger.warning(f"__NEXT_DATA__ not found in detail, retrying ({retry_count+1}/{retry_times}): {response.url}")
                yield scrapy.Request(
                    url=response.url,
                    callback=self.parse_movie_detail,
                    dont_filter=True,
                    meta={**response.meta, 'retry_count': retry_count+1},
                    headers=DEFAULT_REQUEST_HEADERS
                )
            else:
                self.logger.error(f"Persistent failure in detail: {e}")
            return
        try:
            detail_data = json.loads(next_data_json)
            yield from extract_actor_items(detail_data)
        except Exception as e:
            self.logger.error(f'Error parsing detail JSON for {movie_id}: {e}')
            raise
