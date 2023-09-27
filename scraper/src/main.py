from scrapy.crawler import CrawlerProcess
from spiders.career_spider import CareerSpider
import settings

if __name__ == '__main__':
    process = CrawlerProcess(settings=vars(settings))
    process.crawl(CareerSpider)
    process.start()