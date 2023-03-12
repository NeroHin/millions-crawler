# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class MillionsCrawlerPipeline:
    def process_item(self, item, spider):
        
        if item['url_title'] is None:
            item['url_title'] = item['url'].split('/')[-1]
        
        item['url_title'] = item['url_title'].replace('\n', '').replace(
                    '\t\t', '').replace('\t', '')
        
        
        return item

class DuplicateUrlPipeline:
    def __init__(self):
        self.urls_seen = set()
    def process_item(self, item, spider):
        if item['url'] in self.urls_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.urls_seen.add(item['url'])
            return item
        
class SkipItemPipeline:
    '''
    Skip item if the url ends with .pdf, .doc, or .docx
    '''
    def process_item(self, item, spider):
        if item['url'].endswith('.pdf') or item['url'].endswith('.doc') or item['url'].endswith('.docx'):
            raise DropItem("Skip item found: %s" % item)
        else:
            return item
        
class SkipEmailPipeline:
    '''
    Skip item if the url starts with mailto:
    '''
    def process_item(self, item, spider):
        if item['url'].startswith('mailto:'):
            raise DropItem("Skip item found: %s" % item)
        else:
            return item
        
class CompressUrlByMD5Pipeline:
    '''
    Compress url by md5
    '''
    def process_item(self, item, spider):
        import hashlib
        item['url'] = hashlib.md5(item['url'].encode('utf-8')).hexdigest()
        return item
    
class TaiwanEHospitalsPipeline:
    
    def process_item(self, item, spider):
        
        item['article_department'] = item['article_department']
        # TODO from %E6%B5%81%E6%84%9F%E8%AB%AE%E8%A9%A2 -> 流感諮詢
        
        
        return item