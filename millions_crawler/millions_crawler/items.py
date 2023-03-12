# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MillionsCrawlerItem(scrapy.Item):

    # with normal

    url = scrapy.Field()
    title = scrapy.Field()
    
    # with tweh
    article_no = scrapy.Field()
    article_name = scrapy.Field()
    article_question = scrapy.Field()
    articel_answer = scrapy.Field()
    
    
    pass
