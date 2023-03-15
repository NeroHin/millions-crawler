import scrapy
from ..items import Wen8HealthItem
import re
from datetime import datetime
from tqdm import tqdm


class W8hSpider(scrapy.Spider):
    name = "w8h"
    allowed_domains = ["tw.wen8health.com"]
    start_urls = ["https://tw.wen8health.com/"]

    def __init__(self):
        self.base_url = 'https://tw.wen8health.com'
        self.qeustion_url = 'https://tw.wen8health.com/questions/'
        self.last_page_number = 267

    def parse(self, response):

        self.crawler.stats.inc_value('scraped_count')
        
        # check if an hour has passed since the last log
        if datetime.now().minute == 0:
            scraped_count = self.crawler.stats.get_value('scraped_count', 0)
            self.logger.info(f'Crawled {scraped_count} websites in the last hour')


        for page_number in tqdm(range(0, self.last_page_number, 1)):
            yield scrapy.Request(url=self.qeustion_url + str(page_number), callback=self.parse_question_page)

    def parse_question_page(self, response):

        # extract article url into the questions page

        article_url_list = response.css('a::attr(href)').extract()

        for article_url in article_url_list:
            if re.match(r'/question/\d+', article_url):
                yield scrapy.Request(url=self.base_url + article_url, callback=self.parse_article_page)

    def parse_article_page(self, response):

        items = Wen8HealthItem()

        items['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        items['article_url'] = response.url

        # article_no response.url.split('/')[-1]
        items['article_no'] = response.url.split('/')[-1]

        # article_question xpath like //*[@id="__layout"]/div/div[2]/div/div/div/div[1]/h1
        items['article_question'] = response.xpath(
            '//*[@id="__layout"]/div/div[2]/div/div/div/div[1]/h1/text()').extract()

        # article_doctor xpath like //*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div[1]/a/div/div/div[1]/span
        items['article_doctor'] = response.xpath(
            '//*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div[1]/a/div/div/div[1]/span/text()').extract()

        # article_department xpath like //*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div[1]/a/div/div/div[1]/div
        items['article_department'] = response.xpath(
            '//*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div[1]/a/div/div/div[1]/div/text()').extract()

        # article_answer xpath like //*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div[2]/text()
        items['article_answer'] = response.xpath(
            '//*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div[2]/text()').extract()

        yield items
