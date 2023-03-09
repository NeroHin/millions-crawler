import scrapy
import re
from ..items import MillionsCrawlerItem


class WebSpider(scrapy.Spider):
    name = "web"
    # allowed_domains = ["www.ncku.edu.tw", "www.kmu.edu.tw"]
    start_urls = ["http://www.ncku.edu.tw/", "https://www.kmu.edu.tw/"]

    def parse(self, response):

        items = MillionsCrawlerItem()
        for link in response.css('a::attr(href)').extract():

            items['url'] = response.urljoin(link)
            items['title'] = response.css(
                'a[href="'+link+'"]::text').extract_first()

            yield items

        for next_page in response.css('a::attr(href)').extract():
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)


        

            
