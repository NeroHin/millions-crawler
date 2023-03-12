import scrapy
from ..items import TaiwanEHospitalsItem
from tqdm import tqdm

class TwehSpider(scrapy.Spider):
    
    
    name = 'tweh'
    allowed_domains = ['sp1.hso.mohw.gov.tw']

    start_urls = ['https://sp1.hso.mohw.gov.tw/doctor/Index1.php']
    
    def __init__(self):
        self.start_page_number = 1
        

    def parse(self, response):
        
        items = TaiwanEHospitalsItem()
        
        # example the department is in HTML <div class="w3-col l4 m6 s6"><a href="/doctor/All/index.php?d_class=內科" target="_top">內　科</a></div>
        
        department_list = response.css('div.w3-col.l4.m6.s6 a::attr(href)').extract()

        history_page_param = '/doctor/All/history.php?UrlClass='

        
        for department in tqdm(department_list):
            department_name = department.split('=')[1]

            # next I want to extract the history of the department, from /doctor/All/history.php?UrlClass= {{ department }}
            # yield scrapy.Request(url=response.urljoin(history_page + department_name), callback=self.parse_history)
            
            history_page_number = scrapy.Request(url=response.urljoin(history_page_param + department_name), callback=self.parse_history_page_option_value)
            
            
            yield history_page_number
            
    def parse_history_page_option_value(self, response):
        
        # exam//*[@id="PageNo"]/option[ number]
        
        history_page_number = response.css('#PageNo option::attr(value)').extract()
        
        
        if len(history_page_number) == 0:
            yield scrapy.Request(url=response.urljoin(response.url), callback=self.parse_history_article)
        else:
            # start from 1 to the last page
            last_history_page_number = history_page_number[-1]
            
            for page_number in range(self.start_page_number, int(last_history_page_number) + 1):
                yield scrapy.Request(url=response.urljoin(response.url + '&SortBy=q_no&PageNo=' + str(page_number)), callback=self.parse_history_article)
        
        
            
    def parse_history_article(self, response):
        
        items = TaiwanEHospitalsItem()
        # when into this page, I want to extract the history article in the page, pattern is https://sp1.hso.mohw.gov.tw/doctor/All/ShowDetail.php?q_no=193985&SortBy=q_no&PageNo=1
        # the xpath is //*[@id="sidebar-content"]/div/div/div[1]/form/table/tbody/tr[1]/td[7]/a
        article_list = response.css('form table tbody tr td a::attr(href)').extract()
        
        
        
        
        for article in article_list:
            
            # The article doctor xpath is in //*[@id="sidebar-content"]/div/div/div[1]/form/table/tbody/tr[1]/td[3] , such as <td class="text">曹國桃</td>
            article_doctor = response.xpath('//*[@id="sidebar-content"]/div/div/div[1]/form/table/tbody/tr[1]/td[3]/text()').extract_first()
            items['article_doctor'] = article_doctor
            # TODO 目前醫生只抓到第一個，但是有些問題會有多個，需要抓到所有的醫生
            
            items['article_url'] = response.urljoin(article)
            
            # url is https://sp1.hso.mohw.gov.tw/doctor/All/ShowDetail.php?q_no=193985&SortBy=q_no&PageNo=1, I want to extract the 193985
            items['article_no'] = article.split('=')[1].split('&')[0]
            
            # article_department https://sp1.hso.mohw.gov.tw/doctor/All/history.php?UrlClass=%E9%AB%94%E9%81%A9%E8%83%BD&SortBy=q_no&PageNo=13, department is %E9%AB%94%E9%81%A9%E8%83%BD
            items['article_department'] = response.url.split('=')[1].split('&')[0]
            
            # article_question //*[@id="sidebar-content"]/div/div/div[1]/form/table/tbody/tr[1]/td[7]/a text()
            items['article_question'] = response.xpath('//*[@id="sidebar-content"]/div/div/div[1]/form/table/tbody/tr[1]/td[7]/a/text()').extract_first()
            # TODO 目前問題的名稱只抓到第一個，但是有些問題會有多個，需要抓到所有的問題名稱
            
            yield items
            
            article_page = scrapy.Request(url=response.urljoin(article), callback=self.parse_article)
            
            
    def parse_article(self, response):
        
        # when into this page, I want to extract the article information, pattern is https://sp1.hso.mohw.gov.tw/doctor/All/ShowDetail.php?q_no=193985&SortBy=q_no&PageNo=1
        
        item = TaiwanEHospitalsItem()
        
        print()
        
        
        
        