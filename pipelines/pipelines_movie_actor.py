import os
from dotenv import load_dotenv
from data.db_adapter import DBAdapter

load_dotenv()


class PostgresMovieActorPipeline:
    """
    Pipeline for saving movie and actor items to PostgreSQL using DBAdapter.
    Creates tables if needed and logs each save operation.
    """

    def __init__(self, db_type='postgres'):
        """Initialize pipeline with the given database type."""
        self.db_type = db_type
        self.db = None

    def open_spider(self, spider):
        """Open database connection and create tables when spider starts."""
        self.db = DBAdapter(self.db_type)
        self.db.connect()
        self.db.get_table_manager().create_tables(self.db.get_cursor())
        self.db.commit()


    def close_spider(self, spider):
        """Close database connection when spider finishes."""
        self.db.close()


    def process_item(self, item, spider):
        """Save movie or actor item to the database and log the operation."""
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
