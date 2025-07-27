import os
from dotenv import load_dotenv

load_dotenv()


class DBAdapter:
    def __init__(self, db_type='postgres'):
        self.db_type = db_type
        self.conn = None
        self.cur = None
        self.table_manager = None

    def connect(self):
        if self.db_type == 'postgres':
            import psycopg2
            from data.postgres_manager import PostgresManager
            self.conn = psycopg2.connect(os.getenv('POSTGRESQL_URL'))
            self.cur = self.conn.cursor()
            self.table_manager = PostgresManager
        # Future: elif self.db_type == 'mysql':
        #     from data.mysql_table_manager import MySQLTableManager
        #     ...
        #     self.table_manager = MySQLTableManager
        else:
            raise ValueError(f"Unsupported db_type: {self.db_type}")

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def commit(self):
        if self.conn:
            self.conn.commit()

    def execute(self, *args, **kwargs):
        return self.cur.execute(*args, **kwargs)

    def executemany(self, *args, **kwargs):
        return self.cur.executemany(*args, **kwargs)

    def get_cursor(self):
        return self.cur

    def get_table_manager(self):
        return self.table_manager
