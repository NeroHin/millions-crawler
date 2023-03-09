import scrapy


class NckuSpider(scrapy.Spider):
    name = "ncku"
    allowed_domains = ["www.ncku.edu.tw"]
    start_urls = ["http://www.ncku.edu.tw/"]

    def parse(self, response):
        
        for link in response.css('a::attr(href)').extract():
            
            url = response.urljoin(link).replace(' ', '')
            title = response.css('a[href="'+link+'"]::text').extract_first()
            
            if title is None:
                title = url.split('/')[-1]
            
            else:
                title = title.replace('\n', '').replace('\t\t', '').replace('\t', '')
                
                
            yield {
                'url': url,
                'title': title
            }

        
    
