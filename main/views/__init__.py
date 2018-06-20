from flask import Flask, session, g
from main.views import user, item
from main.models import User
from main import application


modules_define = [user.app, item.app]
for app in modules_define:
    application.register_blueprint(app)
