from scrapy.crawler import CrawlerProcess
from spiders.factory import SpiderFactory

if __name__ == "__main__":
    process = CrawlerProcess()
    spider = SpiderFactory.create_spider('imdb_top')
    process.crawl(spider)
    process.start()
