import urllib.request
from bs4 import BeautifulSoup
import re


def get_price(url):
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    price = soup.find("span", id="priceblock_ourprice").string
    return int(re.sub(r'\D', '', price))
