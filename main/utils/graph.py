import matplotlib.pyplot as plt
import random
from main.models import Price
from main import db
import datetime
import matplotlib.dates as mdates


def draw_graph(item_id):
    prices = db.session.query(Price).filter_by(item_id=item_id)
    # X軸データ
    x = [price.scraped_at for price in prices]
    # Y軸データ
    y = [price.body for price in prices]

    # データをセット
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y)

    # グラフのフォーマットの設定
    days = mdates.DayLocator()  # every day
    daysFmt = mdates.DateFormatter('%m/%d')
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(daysFmt)
    fig.autofmt_xdate()
    plt.savefig('main/static/graph/item{}.png'.format(item_id))
    return
