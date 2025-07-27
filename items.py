
import scrapy

class ImdbMovieItem(scrapy.Item):
    movie_id = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    rating = scrapy.Field()
    duration = scrapy.Field()
    metascore = scrapy.Field()

class ImdbActorItem(scrapy.Item):
    actor_id = scrapy.Field()
    movie_id = scrapy.Field()
    name = scrapy.Field()
    isMainCharacter = scrapy.Field()
