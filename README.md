# millions-crawler

This the NCKU course WEB RESOURCE DISCOVERY AND EXPLOITATION homework III, targe is create a crawler application to crawling millions webpage.

![](/image/What%20is%20a%20Web%20Crawler.jpg)
[image source](https://www.simplilearn.com/what-is-a-web-crawler-article)

## Part of the homework:
[Medium Article](https://medium.com/@NeroHin/%E7%88%AC%E8%9F%B2%E6%9C%89%E5%B0%88%E6%94%BB-%E5%88%9D%E6%8E%A2-scrapy-%E7%88%AC%E8%9F%B2-%E4%BB%A5%E7%88%AC%E5%8F%96-15-%E8%90%AC%E7%AD%86%E7%B7%9A%E4%B8%8A%E9%86%AB%E7%99%82%E5%92%A8%E8%A9%A2-qa-%E7%82%BA%E4%BE%8B%E5%AD%90-39a6383a2de4)

# Homework Scope

1. **Crawl millions of webpages**
2. **Remove non-HTML pages**
3. **Performance optimization**
   - How many page can crawl per hour
   - Total time to crawl millions of pages

# Project architecture

### Distributed architecture

![distributed_architecture](./image/scrapy-redis.png)

### Each spider
![spider](./image/Scrapy_architecture.png)

### Spider with [台灣 E 院](https://sp1.hso.mohw.gov.tw/doctor/Index1.php)

![tweh_parse_flowchat](./image/%E8%87%BA%E7%81%A3%20E%20%E9%99%A2%E7%88%AC%E8%9F%B2%E7%B5%90%E6%A7%8B.png)

### Spider with [問 8 健康諮詢](https://tw.wen8health.com/)

![w8h_parse_flowchat](./image/%E5%95%8F%208%20%E5%81%A5%E5%BA%B7%E5%92%A8%E8%A9%A2%E7%88%AC%E8%9F%B2%E7%B5%90%E6%A7%8B.png)

### Spider with [Wiki](https://en.wikipedia.org/wiki/Main_Page)

![wiki_parse_flowchat](./image/Wiki%20%E7%88%AC%E8%9F%B2%E7%B5%90%E6%A7%8B.png)

### Anti-Anti-Spider

1. Skip robot.txt

```bash
# edit settings.py
ROBOTSTXT_OBEY = False
```

2. Use random user-agent

```bash
pip install fake-useragent
```

```python
# edit middlewares.py
class FakeUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = UserAgent()
        request.headers['User-Agent'] = ua.random
```

```python
DOWNLOADER_MIDDLEWARES = {
   "millions_crawler.middlewares.FakeUserAgentMiddleware": 543,
}
```

# Result

## single spider in 2023/03/21

| Spider | Total Page | Total Time (hrs) | Page per Hour |
| :----: | :--------: | :--------------: | :-----------: |
|  tweh  |  152,958   |       1.3        |    117,409    |
|  w8h   |   4,759    |       0.1        |    32,203     |
|  wiki*  | 13,000,320 |       43       |    30,240    |


## distributed spider (4 spider) in 2023/03/24
| Spider | Total Page | Total Time (hrs) | Page per Hour |
| :----: | :--------: | :--------------: | :-----------: |
|  tweh  |  153,288   |       0.52       |    -    |
|  w8h   |   4,921    |       0.16        |    -     |
|  wiki*  | 4,731,249 |       43.2       |    109,492    |


# How to use

0. create a .env file

```bash
bash create_env.sh
```

1. Install [Redis](https://redis.io/)

```bash
sudo apt-get install redis-server
```

2. Install [MongoDB](https://www.mongodb.com/)

```bash
sudo apt-get install mongodb
```

3. Run Redis

```bash
redis-server
```
4. run MongoDB

```bash
sudo service mongod start
```

5. Run spider

```bash
cd millions-crawler
scrapy crawl [$spider_name] # $spider_name = tweh, w8h, wiki
```

# Requirement

```bash
pip install -r requirements.txt
```

# Reference

1. [GitHub | fake-useragent](https://github.com/fake-useragent/fake-useragent)
2. [GitHub | scrapy](https://github.com/scrapy/scrapy)
3. [【Day 20】反反爬蟲](https://ithelp.ithome.com.tw/articles/10224979) 
4. [Documentation of Scrapy](https://docs.scrapy.org/en/latest/index.html)
5. [解决 Redis 之 MISCONF Redis is configured to save RDB snapshots, but is currently not able to persist o...](https://www.jianshu.com/p/3aaf21dd34d6)
6. [Ubuntu Linux 安裝、設定 Redis 資料庫教學與範例](https://officeguide.cc/ubuntu-linux-redis-database-installation-configuration-tutorial-examples/)
7. [如何連線到遠端的 Linux + MongoDB 伺服器？](https://magiclen.org/mongodb-remote)
8. [Scrapy-redis 之終結篇](https://www.twblogs.net/a/5ef9b649952deac88f79c670)