from multiprocessing import Process, Queue
import sqlite3
import scrapy
from scrapy import crawler
from twisted.internet import reactor
from urllib.parse import urlparse
import json


class linkExtractSpider(scrapy.Spider):
    name = "link_extract"
    start_urls = []
    allowed_domains = []
    a = list()

    def __init__(self, url):
        self.start_urls.append(url)
        domain = urlparse(url).netloc
        self.allowed_domains.append(domain)

    # The Parse method will run for each URL in the "start_urls".
    def parse(self, response):

        conn = sqlite3.connect("web_crwler.db")
        # Create the table - only at first time.
        conn.execute(
            '''create table if not existsif not exists links_table (url text, links text)''')

        cur = conn.cursor()

        yield {'url': response.url}
        for link in response.xpath('*//a/@href').getall():
            self.a.append(link)
            yield response.follow(link, self.parse)

        # delete the "no relevant data"
        cur.execute('''DELETE from links_table where url = (?)''',
                    [response.url])
        conn.commit()

        links = json.dumps(self.a)

        cur.execute('''insert into links_table (url, links) values (?, ?)''',
                    (response.url, links))
        conn.commit()


def f(q, URL):
    try:
        runner = crawler.CrawlerRunner()
        deferred = runner.crawl(linkExtractSpider, URL)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


def extract_links(URL):
    q = Queue()
    p1 = Process(target=f, args=(q, URL))
    p1.start()
    result = q.get()
    p1.join()
    if result is not None:
        raise result

    conn = sqlite3.connect("web_crwler.db")
    cur = conn.cursor()
    # read the data from database
    cur.execute("select * from links_table where url = ?", [URL])
    data_from_db = cur.fetchone()
    x = json.loads(data_from_db[1])
    y = set(x)
    return y
