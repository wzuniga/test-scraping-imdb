

from utils.utils import get_imdb_top_url
from spiders.imdb_movie_actor import ImdbTopSpider


class SpiderFactory:
    @staticmethod
    def create_spider(spider_type: str, **kwargs):
        """
        Factory method to instantiate spiders by type.
        Extend this method to add more spiders as needed.
        """
        if spider_type == 'imdb_movies_actors':
            # Default to top url if not provided
            if 'start_urls' not in kwargs:
                kwargs['start_urls'] = [get_imdb_top_url()]
            return ImdbTopSpider(**kwargs)
        # Example for future extension:
        # elif spider_type == 'imdb_actor':
        #     return ImdbActorSpider(**kwargs)
        else:
            raise ValueError(f"Unknown spider type: {spider_type}")
