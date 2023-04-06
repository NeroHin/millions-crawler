import scrapy


class KingnetSpider(scrapy.Spider):
    name = 'kingnet'
    allowed_domains = ['www.kingnet.com.tw']
    start_urls = ['http://www.kingnet.com.tw/']
    
    self.department_domain = 'inquiry/department_all'

    def parse(self, response):
        pass
