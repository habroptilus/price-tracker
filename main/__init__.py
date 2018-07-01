from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

config = {
    "development": "config.Development",
    "production": "config.Production"
}


def configure_app(app):
    # 環境変数を利用して読み込む設定ファイルを決定
    config_name = os.getenv('FLASK_CONFIGURATION', 'production')

    # 設定はオブジェクトとして読み込む
    app.config.from_object(config[config_name])

    # センシティブな設定はインスタンスフォルダ内の設定で上書きする
    app.config.from_pyfile('config.cfg', silent=False)


application = Flask(__name__, instance_relative_config=True)
configure_app(application)
db = SQLAlchemy(application)
