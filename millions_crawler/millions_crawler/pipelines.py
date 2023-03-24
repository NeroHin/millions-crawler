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
import pymongo
from .items import MillionsCrawlerItem

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
        if item['article_url'] in self.urls_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.urls_seen.add(item['article_url'])
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
            cleaned_text = cleaned_text.replace('\r', '').replace('\n', '').replace(
                ' ', '').replace('\\', '').replace('\u3000', '').replace('\xa0', '').replace('\t', '')
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

        # Clean article_name
        if isinstance(item['article_name'], list):
            item['article_name'] = clean_text(item['article_name'])
        else:
            item['article_name'] = clean_text(item['article_name'])

        # extract the doctor name from article_doctor
        item['article_doctor'] = ''.join(item['article_doctor'])
        item['article_doctor'] = re.findall(
            r'／([^，]+),', item['article_doctor'])[0]

        if '／' in item['article_doctor']:
            item['article_doctor'] = item['article_doctor'].split('／')[0]

        # decode article_department, example %E4%B8%AD%E9%86%AB%E7%A7%91 => 中醫科
        item['article_department'] = unquote(item['article_department'])

        # remove the article_no #, example #123456 => 123456, the article_no type is list
        item['article_no'] = ''.join(item['article_no']).replace('#', '')
        
        # use md5 to compress the url
        item['article_url'] = md5(item['article_url'].encode('utf-8')).hexdigest()

        return item


class Wen8HealthPipeline:

    def process_item(self, item, spider):

        def clean_text(text):
            cleaned_text = ''.join(text)
            cleaned_text = cleaned_text.replace('\r', '').replace('\n', '').replace(
                ' ', '').replace('\\', '').replace('\u3000', '').replace('\xa0', '').replace('\t', '')
            return cleaned_text

        # Clean article_answer
        if isinstance(item['article_answer'], list):
            item['article_answer'] = clean_text(item['article_answer'])
        else:
            item['article_answer'] = clean_text(item['article_answer'])

        # Clean article_question
        if isinstance(item['article_question'], list):
            item['article_question'] = clean_text(item['article_question'])
        else:
            item['article_question'] = clean_text(item['article_question'])

        # Clean article_doctor
        if isinstance(item['article_doctor'], list):
            item['article_doctor'] = clean_text(item['article_doctor'])
        else:
            item['article_doctor'] = clean_text(item['article_doctor'])

        # Clean article_department
        if isinstance(item['article_department'], list):
            item['article_department'] = clean_text(item['article_department'])
        else:
            item['article_department'] = clean_text(item['article_department'])

        return item
    
class WikiPipeline:
    
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        
        def clean_text(text):
            cleaned_text = ''.join(text)
            cleaned_text = cleaned_text.replace('\r', '').replace('\n', '').replace(
                ' ', '').replace('\\', '').replace('\u3000', '').replace('\xa0', '').replace('\t', '')
            return cleaned_text
        
        if isinstance(item['url'], list):
            item['url'] = clean_text(item['url'])
        else:
            item['url'] = clean_text(item['url'])
        
        
        if item['url'] in self.urls_seen:
            raise DropItem("Duplicate item found: %s" % item)
        
        # if title equal Permission error, skip the item
        if item['title'] == 'Permission error':
            raise DropItem("Skip item found: %s" % item)

        # if url endwith ip address, skip the item
        if re.match(r'.*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', item['url']):
            raise DropItem("Skip item found: %s" % item)

        # if url have .php, skip the item
        if re.match(r'.*\.php', item['url']):
            raise DropItem("Skip item found: %s" % item)
        
        # use md5 to compress the url
        item['url'] = md5(item['url'].encode('utf-8')).hexdigest()
        
        self.urls_seen.add(item['url'])
        return item

class WikiMongoDBPipeline:

    collection = 'scrapy_items'

    def __init__(self, mongodb_uri, mongodb_db):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('MONGODB_URI'),
            mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # Start with a clean database
        # self.db[self.collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = dict(item)
        self.db[self.collection].insert_one(data)
        return item
    
class TWEHMongoDBPipeline:

    collection = 'tweh_items'

    def __init__(self, mongodb_uri, mongodb_db):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('MONGODB_URI'),
            mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # Start with a clean database
        # self.db[self.collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = dict(item)
        self.db[self.collection].insert_one(data)
        return item
    
class WEN8MongoDBPipeline:

    collection = 'w8h_items'

    def __init__(self, mongodb_uri, mongodb_db):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('MONGODB_URI'),
            mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # Start with a clean database
        # self.db[self.collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = dict(item)
        self.db[self.collection].insert_one(data)
        return item