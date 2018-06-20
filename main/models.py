from main import db
from sqlalchemy.orm import synonym
from werkzeug import check_password_hash, generate_password_hash
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), default='', nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password = db.Column('password', db.String(100),
                          nullable=False)  # privateなフィールド
    items = db.relationship("Item", backref="user",
                            lazy="dynamic", cascade="delete")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)
    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, query, email, password):
        user = query(cls).filter(cls.email == email).first()
        if user is None:
            return None, False
        return user, user.check_password(password)

    def __repr__(self):
        return u'<User id={self.id} email={self.email!r}>'.format(
            self=self)


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    item_name = db.Column(db.String(30), default='', nullable=False)
    url = db.Column(db.String(100), default='', nullable=False)
    lowest_price = db.Column(db.Integer, nullable=False)
    latest_price = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, user_id, item_name, url, lowest_price, latest_price):
        self.user_id = user_id
        self.item_name = item_name
        self.url = url
        self.lowest_price = lowest_price
        self.latest_price = latest_price
        self.update_at = datetime.now


def init_db():
    db.create_all()
    user = User("administrator", "admin@example.com", "admin")
    db.session.add(user)
    db.session.commit()
