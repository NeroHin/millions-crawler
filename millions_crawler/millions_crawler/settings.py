# Scrapy settings for millions_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import datetime
from dotenv import load_dotenv
import os

# load the .env file
load_dotenv()

BOT_NAME = "millions_crawler"

# SCHEDULER = "scrapy_redis.scheduler.Scheduler"

SPIDER_MODULES = ["millions_crawler.spiders"]
NEWSPIDER_MODULE = "millions_crawler.spiders"

#确保所有的爬虫通过Redis去重
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# use .env file to set the redis host and port
REDIS_HOST = str(os.getenv("REDIS_HOST"))
REDIS_PORT = os.getenv("REDIS_PORT")

REDIS_PARAMS = {
    'password': str(os.getenv("REDIS_PASSWORD", None)),
}


# 允許暫停,redis請求記錄不會丟失(重啓爬蟲不會重頭爬取已爬過的頁面)
SCHEDULER_PERSIST = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "millions_crawler (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0
# # The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 100
# CONCURRENT_REQUESTS_PER_IP = 100

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   # "millions_crawler.middlewares.MillionsCrawlerSpiderMiddleware": 543,
   'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # "millions_crawler.middlewares.MillionsCrawlerDownloaderMiddleware": 543,
   "millions_crawler.middlewares.FakeUserAgentMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # "millions_crawler.pipelines.MillionsCrawlerPipeline": 300,
   # "millions_crawler.pipelines.TaiwanEHospitalsPipeline": 300,
   # "millions_crawler.pipelines.Wen8HealthPipeline": 300,
   # "millions_crawler.pipelines.WikiPipeline": 300,
   # "millions_crawler.pipelines.DuplicateUrlPipeline": 350,
   # "millions_crawler.pipelines.SkipItemPipeline": 350,
   # "millions_crawler.pipelines.SkipEmailPipeline": 600,
   # "millions_crawler.pipelines.CompressUrlByMD5Pipeline": 700,
   # 'scrapy_redis.pipelines.RedisPipeline': 400,
   # 'millions_crawler.pipelines.WikiMongoDBPipeline': 300,
   # 'millions_crawler.pipelines.TWEHMongoDBPipeline': 300,
   # 'millions_crawler.pipelines.WEN8MongoDBPipeline': 300,
   # 'millions_crawler.pipelines.KINGNETMongoDBPipeline': 300,
   # "millions_crawler.pipelines.KINGNETPipeline": 300,
   "millions_crawler.pipelines.FamilyDoctorPipeline": 300,
   "millions_crawler.pipelines.FamilyDoctorMongoDBPipeline": 300,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# LOG_LEVEL = 'INFO'

# LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

# LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# # log file with date
# LOG_FILE = 'crawler-{}.log'.format(datetime.datetime.now().strftime('%Y-%m-%d'))

DOWNLOAD_FAIL_ON_DATALOSS = False

# MONGODB CONFIG
MONGODB_URI = str(os.getenv(key="MONGODB_URI"))
MONGODB_DATABASE = str(os.getenv(key="MONGODB_DB_NAME"))