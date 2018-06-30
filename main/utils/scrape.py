import urllib.request
from bs4 import BeautifulSoup
import re
from main.models import User, Item
from main import db


def get_price(url):
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    # price = soup.find("span", id="priceblock_ourprice").string
    price = soup.find_all("span", id=re.compile("priceblock"))[0].string
    return int(re.sub(r'\D', '', price))


def update_price(item_id, now_price):
    item = Item.query.get(item_id)
    item.lowest_price = min(item.lowest_price, now_price)
    item.latest_price = now_price
    item.updated_at = datetime.now()
    db.session.commit()
    return


def updated_items(items):
    for item in items:
        price = get_price(item.url)
        update_price(item.id, price)
    return


def update_all_items():  # これを定期実行する
    items = Item.query.all()
    updated_items(items)
    return


def hello():  # test
    print("hello,world!")
