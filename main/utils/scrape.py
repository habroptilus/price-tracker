import urllib.request
from bs4 import BeautifulSoup
import re

from os import path, pardir
import sys
import os

current_dir = path.abspath(path.dirname(__file__))  # スクリプトのディレクトリ
parent_dir = path.abspath(path.join(current_dir, pardir))  # スクリプトの親ディレクトリ
sys.path.append(parent_dir)


from main.models import Item
from main import db
from datetime import datetime
from main.utils.graph import draw_graph


def get_price(url):
    try:
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        price = soup.find_all("span", id=re.compile("priceblock"))[0].string
        price = price.split("-")[0]
        return int(re.sub(r'\D', '', price))
    except:
        return None


def update_price(item_id, now_price):
    item = Item.query.get(item_id)
    item.lowest_price = min(item.lowest_price, now_price)
    item.latest_price = now_price
    item.updated_at = datetime.now()
    db.session.commit()
    return


def update_items(items):
    for item in items:
        price = get_price(item.url)
        if price is not None:
            update_price(item.id, price)
            draw_graph(item.id)
    return


def update_all_items():  # これを定期実行する
    items = Item.query.all()
    update_items(items)
    return


def hello():  # test
    print("hello,world!")


if __name__ == "__main__":
    hello()
