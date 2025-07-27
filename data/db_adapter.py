import os
from dotenv import load_dotenv

load_dotenv()


class DBAdapter:
    """
    Database adapter for handling connections and operations with different DB engines.
    Currently supports PostgreSQL. Easily extendable for other engines (e.g., MySQL).
    """
    def __init__(self, db_type='postgres'):
        """Initialize the adapter with the specified database type."""
        self.db_type = db_type
        self.conn = None
        self.cur = None
        self.table_manager = None

    def connect(self):
        """Establish a connection to the database and set up the table manager."""
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
        """Close the database cursor and connection."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def commit(self):
        """Commit the current transaction."""
        if self.conn:
            self.conn.commit()

    def execute(self, *args, **kwargs):
        """Execute a single SQL statement."""
        return self.cur.execute(*args, **kwargs)

    def executemany(self, *args, **kwargs):
        """Execute a SQL command against all parameter sequences provided."""
        return self.cur.executemany(*args, **kwargs)

    def get_cursor(self):
        """Return the current database cursor."""
        return self.cur

    def get_table_manager(self):
        """Return the table manager class for the current DB type."""
        return self.table_manager
