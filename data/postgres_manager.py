class PostgresManager:
    """
    PostgreSQL manager for IMDb tables and records.
    Provides methods to create tables and insert movies and actors.
    """
    @staticmethod
    def create_tables(cur):
        """Create imdb_movies and imdb_actors tables if they do not exist."""
        cur.execute('''
            CREATE TABLE IF NOT EXISTS imdb_movies (
                movie_id TEXT PRIMARY KEY,
                title TEXT,
                year INT,
                rating FLOAT,
                duration INT,
                metascore INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS imdb_actors (
                actor_id TEXT,
                movie_id TEXT,
                name TEXT,
                isMainCharacter BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (actor_id, movie_id)
            )
        ''')

    @staticmethod
    def insert_movie(cur, item):
        """Insert or update a movie record in imdb_movies."""
        cur.execute('''
            INSERT INTO imdb_movies (movie_id, title, year, rating, duration, metascore)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (movie_id) DO UPDATE SET
                title=EXCLUDED.title,
                year=EXCLUDED.year,
                rating=EXCLUDED.rating,
                duration=EXCLUDED.duration,
                metascore=EXCLUDED.metascore
        ''', (
            item.get('movie_id'),
            item.get('title'),
            item.get('year'),
            item.get('rating'),
            item.get('duration'),
            item.get('metascore')
        ))

    @staticmethod
    def insert_actor(cur, item):
        """Insert or update an actor record in imdb_actors."""
        cur.execute('''
            INSERT INTO imdb_actors (actor_id, movie_id, name, is_main_character)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (actor_id, movie_id) DO UPDATE SET
                name=EXCLUDED.name,
                is_main_character=EXCLUDED.is_main_character
        ''', (
            item.get('actor_id'),
            item.get('movie_id'),
            item.get('name'),
            item.get('isMainCharacter')
        ))
