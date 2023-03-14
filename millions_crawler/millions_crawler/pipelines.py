# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from hashlib import md5
from urllib.parse import unquote
import re
import unicodedata as ucd

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

        item['url'] = md5(item['url'].encode('utf-8')).hexdigest()
        return item
    
class TaiwanEHospitalsPipeline:
    
    def process_item(self, item, spider):
        
        
        def clean_text(text):
            cleaned_text = ''.join(text)
            cleaned_text = cleaned_text.replace('\r', '').replace('\n', '').replace(' ', '').replace('\\', '').replace('\u3000', '').replace('\xa0', '').replace('\t', '')
            return cleaned_text
        
        # Clean article_answer
        if isinstance(item['article_answer'], list):
            item['article_answer'] = clean_text(item['article_answer'])
        else:
            item['article_answer'] = clean_text(item['article_answer'])
            
        # Clean article_content
        if isinstance(item['article_content'], list):
            item['article_content'] = clean_text(item['article_content'])
        else:
            item['article_content'] = clean_text(item['article_content'])
            
        # extract the doctor name from article_doctor
        doctors = ''.join(item['article_doctor'])
        item['article_doctor'] = re.findall(r'／(.+?),', doctors)[0]
        
        # decode article_department, example %E4%B8%AD%E9%86%AB%E7%A7%91 => 中醫科
        item['article_department'] = unquote(item['article_department'])

        return item
    