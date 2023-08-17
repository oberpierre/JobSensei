from scrapy.crawler import CrawlerProcess
from scraper.src.spiders.quotes_spider import QuotesSpider

if __name__ == '__main__':
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json'
    })

    process.crawl(QuotesSpider)
    process.start()