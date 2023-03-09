import scrapy


class NckuSpider(scrapy.Spider):
    name = "ncku"
    allowed_domains = ["www.ncku.edu.tw"]
    start_urls = ["http://www.ncku.edu.tw/"]

    def parse(self, response):
        pass
