import scrapy
from ..items import WikiItem
from datetime import datetime

class WikiSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["http://en.wikipedia.org/"]

    def parse(self, response):

        self.crawler.stats.inc_value('scraped_count')
        
        # check if an hour has passed since the last log
        if datetime.now().minute == 0:
            scraped_count = self.crawler.stats.get_value('scraped_count', 0)
            self.logger.info(f'Crawled {scraped_count} websites in the last hour')

        items = WikiItem()
        
        link_list = response.css('a::attr(href)').extract()
        
        for link in link_list:
            if link.startswith('/wiki/'):
                url = response.urljoin(link)
                items['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                items['url'] = url
                items['title'] = url.split('/')[-1]
                yield items
                yield scrapy.Request(url=url, callback=self.parse)
                
                
                
                

        

        
