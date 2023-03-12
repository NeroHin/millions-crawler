# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MillionsCrawlerItem(scrapy.Item):

    # with normal

    url = scrapy.Field()
    url_title = scrapy.Field()
    
    pass

class TaiwanEHospitalsItem(scrapy.Item):
    # with tweh
    article_department = scrapy.Field()
    article_doctor = scrapy.Field()
    article_url = scrapy.Field()
    article_no = scrapy.Field()
    article_name = scrapy.Field()
    article_question = scrapy.Field()
    article_answer = scrapy.Field()
    pass
