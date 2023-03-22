from scrapy_redis.spiders import RedisSpider 
import scrapy
from ..items import WikiItem
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

class WikiSpider(RedisSpider):
    name = "wiki-redis"
    allowed_domains = ["en.wikipedia.org"]
    # start_urls = ["http://en.wikipedia.org/"]
    
    # redis_key = "wiki:start_urls"
    redis_key = "wiki"
    # crawled_urls = set()


    def parse(self, response):
        # if response.url in self.crawled_urls:
        #     return

        # self.crawled_urls.add(response.url)

        items = WikiItem()
        items['url'] = response.url
        items['title'] = response.css('title::text').get()
        items['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # return dict of items
        yield items

        link_list = response.css('a::attr(href)').extract()
        for link in link_list:
            if link.startswith('/wiki/'):
                url = response.urljoin(link)
                yield scrapy.Request(url=url, callback=self.parse)
