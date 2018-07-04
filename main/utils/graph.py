import matplotlib.pyplot as plt
import random
from main.models import Price
from main import db
import matplotlib.dates as mdates
import os
import glob
from datetime import datetime


def draw_graph(item_id):

    # 以前のグラフを消去
    path_list = glob.glob('main/static/graph/item{}*'.format(item_id))
    print(path_list)
    for path in path_list:
        os.remove(path)

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
    # ハッシュ値の計算
    now = datetime.now()
    hash_value = now.strftime("%Y%m%d%H%M%S")
    plt.savefig('main/static/graph/item{}_{}.png'.format(item_id, hash_value))
    return
