import urllib.request
from bs4 import BeautifulSoup
import re
from main.models import Item, Price
from main import db
from datetime import datetime
from main.utils.graph import draw_graph


def get_price(url):
    try:
        # 通常の商品の場合
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        price = soup.find_all("span", id=re.compile("priceblock"))[0].string
        price = price.split("-")[0]
        return int(re.sub(r'\D', '', price))
    except:
        try:
            # 書籍
            soup = BeautifulSoup(
                urllib.request.urlopen(url).read(), "html.parser")
            price = soup.find_all(
                "span", class_="a-size-medium a-color-price offer-price a-text-normal")[0].string
            price = price.split("-")[0]
            return int(re.sub(r'\D', '', price))
        except:
            try:
                # kindle
                soup = BeautifulSoup(
                    urllib.request.urlopen(url).read(), "html.parser")
                price = soup.find_all(
                    "span", class_="a-size-base a-color-price a-color-price")[0].string
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
    p = Price(item.id, now_price)
    db.session.add(p)
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
    print("hello world!")
