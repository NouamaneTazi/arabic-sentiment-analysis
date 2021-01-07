from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
import scrapy
import pandas as pd
import logging
start_urls = pd.read_csv('links.csv').link.to_list()

class AmazonReviewsSpider(scrapy.Spider):
    name = 'amazon_reviews'
    allowed_domains = ['amazon.sa']
    start_urls = start_urls
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

    def parse(self, response):
        data = response.css('#cm_cr-review_list')
        star_rating = data.css('.review-rating')
        comments = data.css('.review-text')
        count = 0
        for review in star_rating:
            yield {'stars': ''.join(review.xpath('.//text()').extract()),
                    'comment': ''.join(comments[count].xpath(".//text()").extract())
                    }
            count += 1
        next_page = response.css('.a-last a ::attr(href)').extract_first()
        if next_page :
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
logger = logging.getLogger('scrapy.core.scraper')
logger.setLevel('INFO')
runner = CrawlerRunner(settings={
    "FEEDS": {
        "reviews2.csv": {"format": "csv"},
    },
})

d = runner.crawl(AmazonReviewsSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()  # the script will block here until the crawling is finished
