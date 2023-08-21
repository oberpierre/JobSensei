from scrapy.crawler import CrawlerProcess
from spiders.career_spider import CareerSpider

if __name__ == '__main__':
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json'
    })

    process.crawl(CareerSpider)
    process.start()