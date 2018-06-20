from flask import Blueprint, redirect, flash, session, g
from flask import render_template, request, url_for
from main.models import User
from main import db
from functools import wraps
from main.views.utils import login_required, login_user_check

app = Blueprint("user", __name__)


@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(session['user_id'])


@app.route("/signup", methods=["GET", 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if username:
            user = User(username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.show_user', user.id))
        else:
            return redirect(url_for('user.login'))
    return render_template("signup.html")


@app.route("/user/<int:user_id>")
@login_required
def mypage(user_id):
    login_user_check(user_id)
    target_user = User.query.get(user_id)  # primary keyでなら検索できる
    return render_template("mypage.html", target_user=target_user)


@app.route("/user/delete/<int:user_id>", methods=['POST'])
def del_user(user_id):
    target_user = User.query.get(user_id)  # primary keyでなら検索できる
    db.session.delete(target_user)
    db.session.commit()
    return redirect(url_for("user.login"))


@app.route("/user/edit/<int:user_id>", methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    target_user = User.query.get(user_id)  # primary keyでなら検索できる
    if request.method == 'GET':
        login_user_check(user_id)
        return render_template("edit_user.html", target_user=target_user)
    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        target_user.username = username
        target_user.email = email
        target_user.password = password
        db.session.commit()
        return redirect(url_for("user.mypage", user_id=user_id))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user, authenticated = User.authenticate(db.session.query,
                                                request.form['email'], request.form['password'])
        if authenticated:
            session['user_id'] = user.id
            flash('You were logged in')
            return redirect(url_for('user.mypage', user_id=user.id))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('user.login'))
