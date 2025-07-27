
"""
Script to run a Scrapy spider using the Factory pattern.
Creates and starts the selected spider programmatically.
"""

from scrapy.crawler import CrawlerProcess
from spiders.factory import SpiderFactory

if __name__ == "__main__":
    process = CrawlerProcess()  # Initialize Scrapy process
    spider = SpiderFactory.create_spider('imdb_top')  # Create spider instance
    process.crawl(spider)  # Schedule the spider
    process.start()  # Start crawling
