from flask import Flask, session, g
from main.views import user
from main.models import User
from main import application


modules_define = [user.app]
for app in modules_define:
    application.register_blueprint(app)
