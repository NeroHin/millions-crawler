import scrapy
from ..items import FamilyDoctorItem
from datetime import datetime

class FamilyDoctorSpider(scrapy.Spider):
    name = 'familydoctor'
    allowed_domains = ['familydoctor.com.cn']

    def start_requests(self):
        base_url = 'https://www.familydoctor.com.cn/q/{}.html'
        for page_num in range(9631000, 20429275):
            url = base_url.format(page_num)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        items = FamilyDoctorItem()
        
        
        items['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        items['article_question'] = response.xpath('/html/body/div[4]/div/div[1]/div[1]/div/div[2]/p[1]/text()').get()
        items['article_answer'] = response.xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li/div[2]/dl/dd/p/text()').getall()
        items['article_doctor'] = response.xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li/div[2]/dl/dt/a[1]/p/text()').get()
        items['article_url'] = response.url
        
        yield items


