import matplotlib.pyplot as plt
import random
from main.models import Price, Item
from main import db
import matplotlib.dates as mdates
import os
import glob
from datetime import datetime, timedelta


"""
グラフ作成に必要なスクレイピング期間
"""
period_hour = 1
period_min = 10


def draw_graph(item_id):

    # グラフの作成
    prices = list(db.session.query(Price).filter_by(item_id=item_id))
    prices = sorted(prices, key=lambda x: x.scraped_at)
    oldest_time = prices[0].scraped_at
    latest_time = prices[-1].scraped_at
    if oldest_time + timedelta(minutes=period_min) > latest_time:
        return
    # 以前のグラフを消去
    path_list = glob.glob('main/static/graph/item{}*'.format(item_id))
    for path in path_list:
        os.remove(path)

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
