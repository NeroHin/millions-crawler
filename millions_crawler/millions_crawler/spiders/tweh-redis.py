import scrapy
from scrapy_redis.spiders import RedisSpider
from ..items import TaiwanEHospitalsItem
from tqdm import tqdm
from datetime import datetime


class TwehSpider(RedisSpider):
    name = 'tweh-redis'
    allowed_domains = ['sp1.hso.mohw.gov.tw']
    redis_key = 'tweh'
    start_page_number = 1
    # SCHEDULER_FLUSH_ON_START = True

    def parse(self, response):

        # example the department is in HTML <div class="w3-col l4 m6 s6"><a href="/doctor/All/index.php?d_class=內科" target="_top">內　科</a></div>
        department_list = response.css('div.w3-col.l4.m6.s6 a::attr(href)').extract()

        history_page_param = '/doctor/All/history.php?UrlClass='

        for department in tqdm(department_list):
            department_name = department.split('=')[1]

            # next I want to extract the history of the department, from /doctor/All/history.php?UrlClass= {{ department }}
            # yield scrapy.Request(url=response.urljoin(history_page + department_name), callback=self.parse_history)

            history_page_number = scrapy.Request(url=response.urljoin(history_page_param + department_name), callback=self.parse_history_page_option_value)

            yield scrapy.Request(url=response.urljoin(history_page_param + department_name), callback=self.parse_history_page_option_value, dont_filter=True)

    def parse_history_page_option_value(self, response):
        # exam//*[@id="PageNo"]/option[ number]
        history_page_number = response.css('#PageNo option::attr(value)').extract()

        if len(history_page_number) == 0:
            yield scrapy.Request(url=response.urljoin(response.url), callback=self.parse_history_article, dont_filter=True)
        else:
            # start from 1 to the last page
            last_history_page_number = history_page_number[-1]

            for page_number in range(self.start_page_number, int(last_history_page_number) + 1):
                yield scrapy.Request(url=response.urljoin(response.url + '&SortBy=q_no&PageNo=' + str(page_number)), callback=self.parse_history_article)

    def parse_history_article(self, response):

        items = TaiwanEHospitalsItem()
        # when into this page, I want to extract the history article in the page, pattern is https://sp1.hso.mohw.gov.tw/doctor/All/ShowDetail.php?q_no=193985&SortBy=q_no&PageNo=1
        # the xpath is //*[@id="sidebar-content"]/div/div/div[1]/form/table/tbody/tr[1]/td[7]/a
        article_list = response.css(
            'form table tbody tr td a::attr(href)').extract()

        for article in article_list:


            # article_department https://sp1.hso.mohw.gov.tw/doctor/All/history.php?UrlClass=%E9%AB%94%E9%81%A9%E8%83%BD&SortBy=q_no&PageNo=13, department is %E9%AB%94%E9%81%A9%E8%83%BD
            items['article_department'] = response.url.split('=')[
                1].split('&')[0]

            yield scrapy.Request(url=response.urljoin(article), callback=self.parse_article, meta={'item': items})

    def parse_article(self, response):

        # when into this page, I want to extract the article information, pattern is https://sp1.hso.mohw.gov.tw/doctor/All/ShowDetail.php?q_no=193985&SortBy=q_no&PageNo=1

        items = response.meta['item']
        
        items['crawl_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        items['article_url'] = response.url

        # article_no xpath like /html/body/div/div/div/div/div[2]/div[1]/div[1]/h2
        items['article_no'] = response.xpath(
            '/html/body/div/div/div/div/div[2]/div[1]/div[1]/h2/text()').extract()

        # article_name xpath like /html/body/div/div/div/div/div[2]/div[1]/div[2]/h2
        items['article_name'] = response.xpath(
            '/html/body/div/div/div/div/div[2]/div[1]/div[2]/h2/text()').extract()

        # article_doctor xpath like /html/body/div/div/div/div/div[2]/div[3]/div[1]/div[2]/div
        items['article_doctor'] = response.xpath(
            '/html/body/div/div/div/div/div[2]/div[3]/div[1]/div[2]/div/text()').extract()

        # article_content xpath like /html/body/div/div/div/div/div[2]/div[2]/div[2]/div
        items['article_content'] = response.xpath(
            '/html/body/div/div/div/div/div[2]/div[2]/div[2]/div/text()').extract()

        # article_answer xpath like /html/body/div/div/div/div/div[2]/div[3]/div[2]/div
        items['article_answer'] = response.xpath(
            '/html/body/div/div/div/div/div[2]/div[3]/div[2]/div/text()').extract()

        yield items
