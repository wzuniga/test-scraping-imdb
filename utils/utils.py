# moved from project root
import os
import logging
from dotenv import load_dotenv

def get_logger(name):
    """
    Returns a logger with the given name, configured for console output.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def get_env_variable(var_name, default=None):
    """
    Loads .env and returns the value of the given environment variable.
    Returns default if not found.
    """
    load_dotenv()
    return os.getenv(var_name, default)

def get_imdb_top_url():
    """
    Returns the IMDb top URL from environment or default value.
    """
    return get_env_variable('IMDB_TOP_URL', 'https://www.imdb.com/chart/top/')
