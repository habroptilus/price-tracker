from flask import render_template, request, url_for, redirect, session, g
from main.models import User, Item
from main import db
from functools import wraps
from datetime import datetime, timedelta
from main.utils.scrape import get_price

DAY = 1  # 何日おきにスクレイピングするか


def login_required(f):  # デコレーターを定義。fはデコレートされるメソッド
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if g.user is None:  # ログインしてなかったらログイン画面にリダイレクト
            return redirect(url_for('user.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_view


def login_user_check(user_id):  # ログインユーザーと異なるページを見ようとしたらログイン画面に戻される
    if g.user.id != user_id:
        return redirect(url_for("user.login"))


def update_price(item_id, now_price):
    item = Item.query.get(item_id)
    item.lowest_price = min(item.lowest_price, now_price)
    item.latest_price = now_price
    item.updated_at = datetime.now()
    db.session.commit()
    return item


def updated_items(items):
    updated = []
    for item in items:
        if item.updated_at + timedelta(days=DAY) < datetime.now():
            price = get_price(item.url)
            updated_item = update_price(item.id, price)
            updated.append(updated_item)
        else:
            updated.append(item)
    return updated
