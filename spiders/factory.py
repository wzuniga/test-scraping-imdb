from utils.utils import get_imdb_top_url
from spiders.imdb_movie_actor import ImdbTopSpider


class SpiderFactory:
    """
    Factory for creating Scrapy spider instances by type.
    Extendable for additional spiders.
    """

    @staticmethod
    def create_spider(spider_type: str, **kwargs):
        """
        Instantiate a spider based on the given type.
        Returns a configured spider instance.
        """
        if spider_type == 'imdb_movies_actors':
            # Use default top URL if not provided
            if 'start_urls' not in kwargs:
                kwargs['start_urls'] = [get_imdb_top_url()]
            return ImdbTopSpider(**kwargs)
        # Example for future extension:
        # elif spider_type == 'imdb_actor':
        #     return ImdbActorSpider(**kwargs)
        else:
            raise ValueError(f"Unknown spider type: {spider_type}")
