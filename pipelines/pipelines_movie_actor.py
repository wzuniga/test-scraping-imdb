
import os
from dotenv import load_dotenv
from data.db_adapter import DBAdapter

load_dotenv()

class PostgresMovieActorPipeline:

    def __init__(self, db_type='postgres'):
        self.db_type = db_type
        self.db = None

    def open_spider(self, spider):
        self.db = DBAdapter(self.db_type)
        self.db.connect()
        self.db.get_table_manager().create_tables(self.db.get_cursor())
        self.db.commit()


    def close_spider(self, spider):
        self.db.close()


    def process_item(self, item, spider):
        cur = self.db.get_cursor()
        tm = self.db.get_table_manager()
        if item.__class__.__name__ == 'ImdbMovieItem':
            tm.insert_movie(cur, item)
            self.db.commit()
            spider.logger.info(f'Saved movie on imdb_movies: {item.get("movie_id")} - {item.get("title")}')
        elif item.__class__.__name__ == 'ImdbActorItem':
            tm.insert_actor(cur, item)
            self.db.commit()
            spider.logger.info(f'Saved actor on imdb_actors: {item.get("actor_id")} - {item.get("name")}')
        return item
