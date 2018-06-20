from flask import Blueprint, redirect, flash, session, g
from flask import render_template, request, url_for
from main.models import User, Item
from main import db
from functools import wraps
from main.views.utils import login_required, login_user_check
from datetime import datetime
from main.views import user

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
        latest_price = 10000
        lowest_price = 1000
        if item_name:
            item = Item(user_id, item_name, url, latest_price, lowest_price)
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('user.mypage', user_id=user_id))
        else:
            return redirect(url_for("item.register", user_id=user_id))
    return render_template("item_register.html", user_id=user_id)


@app.route("/item/<int:item_id>")
def show(item_id):
    item = Item.query.get(item_id)  # primary keyでなら検索できる
    if item:
        return render_template("show_item.html", item=item)
    return redirect(url_for("user.login"))
