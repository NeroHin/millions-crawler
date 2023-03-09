import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from ..items import MillionsCrawlerItem



class NckuSpider(scrapy.Spider):
    name = "ncku"
    allowed_domains = ["www.ncku.edu.tw"]
    start_urls = ["http://www.ncku.edu.tw/"]
    pdf_pattern = re.compile(r'.*\.pdf$')

    def parse(self, response):

        items = MillionsCrawlerItem()
        for link in response.css('a::attr(href)').extract():

            items['url'] = response.urljoin(link)
            items['title'] = response.css('a[href="'+link+'"]::text').extract_first()


            yield (items)

        

