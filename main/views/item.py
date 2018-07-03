from flask import Blueprint, redirect, flash, session, g
from flask import render_template, request, url_for
from main.models import User, Item, Price
from main import db
from functools import wraps
from main.views.utils import login_required, login_user_check
from datetime import datetime
from main.views import user
from main.utils.scrape import get_price, update_items
from main.utils.graph import draw_graph

app = Blueprint("item", __name__)


@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(session['user_id'])


@app.route("/item/create/<int:user_id>", methods=["GET", 'POST'])
def register(user_id):
    login_user_check(user_id)
    if request.method == "POST":
        user_id = user_id
        item_name = request.form.get('item_name')
        url = request.form.get('url')
        price = get_price(url)
        if price is None:
            flash("商品価格の取得に失敗しました。", "info")
            return redirect(url_for("item.register", user_id=user_id))
        latest_price = price
        lowest_price = price
        if item_name:
            item = Item(user_id, item_name, url, latest_price, lowest_price)
            db.session.add(item)
            db.session.commit()
            p = Price(item.id, price)
            db.session.add(p)
            db.session.commit()
            draw_graph(item.id)
            return redirect(url_for('user.mypage', user_id=user_id))
        else:
            return redirect(url_for("item.register", user_id=user_id))
    return render_template("item_register.html", user_id=user_id)


@app.route("/item/<int:item_id>")
def show(item_id):
    item = Item.query.get(item_id)  # primary keyでなら検索できる
    user = User.query.get(item.user_id)
    login_user_check(user.id)
    prices = db.session.query(Price).filter_by(item_id=item_id)
    if item:
        return render_template("show_item.html", item=item, prices=prices)
    return redirect(url_for("user.login"))


@app.route("/item/edit/<int:item_id>", methods=["GET", 'POST'])
def edit(item_id):
    item = Item.query.get(item_id)  # primary keyでなら検索できる
    user = User.query.get(item.user_id)
    login_user_check(user.id)
    if request.method == "POST":
        item_name = request.form.get('item_name')
        url = request.form.get('url')
        item.item_name = item_name
        item.url = url
        db.session.commit()
        return redirect(url_for("item.show", item_id=item.id))
    return render_template("edit_item.html", item=item)


@app.route("/item/delete/<int:item_id>", methods=["POST"])
def delete(item_id):
    item = Item.query.get(item_id)
    user = User.query.get(item.user_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("user.mypage", user_id=user.id))


@app.route("/item/update_all/<int:user_id>")
def update_all(user_id):
    items = db.session.query(Item).filter_by(user_id=user_id)
    update_items(items)
    return redirect(url_for("user.mypage", user_id=user_id))
