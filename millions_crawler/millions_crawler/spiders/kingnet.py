import scrapy


class KingnetSpider(scrapy.Spider):
    name = 'kingnet'
    allowed_domains = ['www.kingnet.com.tw']
    start_urls = ['https://www.kingnet.com.tw']
    
    def __init__(self):
        self.article_list = 'https://www.kingnet.com.tw/inquiry/list?sectionId='

        

    def parse(self, response):

        for section_id in range(1, 126, 1):
            yield scrapy.Request(url=self.article_list + str(section_id), callback=self.parse_article_list)
            
    def parse_article_list(self, response):
        
        # extract <h6 class="media-heading"> url
        article_url_list = response.css('h6.media-heading a::attr(href)').extract()
        
    # TODO 目前有發現可以透過 API 取得文章內容
    # https://www.kingnet.com.tw/ajax/selectInquiryList?sectionId=1&keyword=&inquiryStatus=Y&dataIndex=2&dataCnt=10
    # *花點時間來研究一下 API 的使用方式
        
       
        
        