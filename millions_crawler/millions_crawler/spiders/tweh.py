import scrapy
from ..items import MillionsCrawlerItem
from tqdm import tqdm

class TwehSpider(scrapy.Spider):
    name = 'tweh'
    allowed_domains = ['sp1.hso.mohw.gov.tw']

    # department list
    department_list = ["神經內科", "神經外科", "胸腔內科", "整型外科", "肝膽腸胃科", "潛水醫學科", 
                       "核子醫學科", "心臟血管專科", "乳房甲狀腺科", "產後憂鬱諮詢", "內科", "牙科", 
                       "外科", "兒科", "骨科", "眼科", "漢生病", "中醫科", "皮膚科", "泌尿科", 
                       "家醫科", "高年科", "婦產科", "麻醉科", "復健科", "腫瘤科", "精神科", 
                       "體適能", "營養教室", "戒菸諮詢", "藥物諮詢", "流感諮詢", "耳鼻喉科", "罕見疾病", "放射線科"]

    start_urls = ['https://sp1.hso.mohw.gov.tw/doctor/Index1.php']

    def parse(self, response):
        
        item = MillionsCrawlerItem()
        
        # example the department is in HTML <div class="w3-col l4 m6 s6"><a href="/doctor/All/index.php?d_class=內科" target="_top">內　科</a></div>
        
        department_list = response.css('div.w3-col.l4.m6.s6 a::attr(href)').extract()
        
        history_page = '/doctor/All/history.php?UrlClass='
        
        for department in tqdm(department_list):
            department_name = department.split('=')[1]

            # next I want to extract the history of the department, from /doctor/All/history.php?UrlClass= {{ department }}
            yield scrapy.Request(url=response.urljoin(history_page + department_name), callback=self.parse_history)
            
    def parse_history(self, response):
        
        # when into this page, I want to extract the history article in the page, pattern is https://sp1.hso.mohw.gov.tw/doctor/All/ShowDetail.php?q_no=193985&SortBy=q_no&PageNo=1
        # the xpath is //*[@id="sidebar-content"]/div/div/div[1]/form/table/tbody/tr[1]/td[7]/a
        
        article_list = response.css('form table tbody tr td a::attr(href)').extract()
        
        for article in article_list:
            print(scrapy.Request(url=response.urljoin(article)))
       