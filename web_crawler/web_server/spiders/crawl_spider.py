import scrapy
import sqlite3
import datetime
from scrapy import crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor


class crawlSpider(scrapy.Spider):

    name = "crawl"
    start_urls = []

    def __init__(self, url):
        self.start_urls.append(url)

    def parse(self, response):

        conn = sqlite3.connect("web_crwler.db")
        # Create the table - only at first time.
        conn.execute(
            '''create table if not exists my_table (url text, html text, last_seen timestamp)''')

        cur = conn.cursor()
        # delete the object from table (if exists)
        cur.execute('''DELETE from my_table where url = (?)''', [response.url])
        conn.commit()

        cur.execute('''insert into my_table (url, html, last_seen) values (?, ?, ?)''',
                    (response.url, response.body, datetime.datetime.now().ctime()))
        conn.commit()


def f(q, URL):
    try:
        runner = crawler.CrawlerRunner()
        deferred = runner.crawl(crawlSpider, URL)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


def fetch_and_save_page(URL):
    q = Queue()
    p = Process(target=f, args=(q, URL))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

    conn = sqlite3.connect("web_crwler.db")
    cur = conn.cursor()
    # read the data from database
    cur.execute("select * from my_table where url = ?", [URL])
    data_from_db = cur.fetchone()
    x = data_from_db[1]
    return x
