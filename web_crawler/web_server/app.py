from flask import Flask
from datetime import datetime
from scrapy.crawler import CrawlerProcess
import sqlite3
from spiders.crawl_spider import *
from spiders.link_extract_spider import extract_links
from json import dumps
from json import JSONEncoder
app = Flask(__name__)


class set_encoder(JSONEncoder):
    def default(self, obj):
        return list(obj)


@app.route('/')
def func():
    return 'My Web Crawler'


@app.route('/crawl/<path:URL>', methods=['GET'])
def crawl(URL: str):

    html_content = fetch_and_save_page(URL)
    links_from_url = extract_links(str(URL))
    json_data = dumps(links_from_url, indent=4, cls=set_encoder)
    return json_data


@app.route('/last_seen/<path:URL>', methods=['GET'])
def last_seen(URL: str):

    conn = sqlite3.connect("web_crwler.db")
    # Create the table - only at first time.
    conn.execute(
        '''create table if not exists my_table (url text, html text, last_seen timestamp)''')

    cur = conn.cursor()
    # read the data from database
    cur.execute("select * from my_table where url = ?", [URL])
    data_from_db = cur.fetchone()
    if data_from_db[2] is not None:
        return f'Last Seen: {data_from_db[2]}'

    return f'Last Seen: Never Seen'


def main():
    app.run()


if __name__ == '__main__':
    main()
