from flask import render_template, request, url_for, redirect, session, g
from main.models import User, Item
from main import db
from functools import wraps
from datetime import datetime, timedelta


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
