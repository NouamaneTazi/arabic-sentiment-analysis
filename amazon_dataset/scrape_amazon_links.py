from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
import scrapy

categories = ['amazon-devices', 'videogames', 'home-improvement', 'electronics', 'beauty', 'grocery', 'automotive', 'health',
              'garden', 'sports-goods', 'office-products', 'home', 'gift-cards', 'toys', 'books', 'pet-supplies', 'fashion', 'baby-products']
n_items_per_cat = 2


class AmazonLinksSpider(scrapy.Spider):
    name = 'amazon_links'
    allowed_domains = ['amazon.sa']
    start_urls = ['https://www.amazon.sa/gp/bestsellers/' +
                  category for category in categories]

    def parse(self, response):
        items = response.css('.aok-inline-block.zg-item')
        for item in items[:n_items_per_cat]:
            link = item.css('.a-link-normal ::attr(href)').extract_first()
            link = '/'.join(link.split('/')[3:])
            yield {'link': 'https://www.amazon.sa/product-reviews/' + link}


configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s', 'LOG_LEVEL': 'ERROR'})
runner = CrawlerRunner(settings={
    "FEEDS": {
        "links.csv": {"format": "csv"},
    },
})

d = runner.crawl(AmazonLinksSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()  # the script will block here until the crawling is finished
