
import scrapy

class ImdbMovieItem(scrapy.Item):
    """
    Scrapy item for storing IMDb movie data fields.
    """
    movie_id = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    rating = scrapy.Field()
    duration = scrapy.Field()
    metascore = scrapy.Field()

class ImdbActorItem(scrapy.Item):
    """
    Scrapy item for storing IMDb actor data fields.
    """
    actor_id = scrapy.Field()
    movie_id = scrapy.Field()
    name = scrapy.Field()
    isMainCharacter = scrapy.Field()
