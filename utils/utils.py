# moved from project root
import os
import logging
from dotenv import load_dotenv

def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def get_env_variable(var_name, default=None):
    load_dotenv()
    return os.getenv(var_name, default)

def get_imdb_top_url():
    return get_env_variable('IMDB_TOP_URL', 'https://www.imdb.com/chart/top/')
