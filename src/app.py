import logging

import sentry_sdk
from flask import Flask

from config import settings
from db import connect
from views.index import IndexView
from views.statii import StatiiView

FORMAT = "* %(asctime)s - %(levelname)-8s * %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)


if settings.SENTRY_DSN:
    sentry_sdk.init(settings.SENTRY_DSN, environment=settings.ENVIRONMENT)


def create_app():
    app = Flask(__name__)
    app.add_url_rule("/", view_func=IndexView.as_view("index"))
    app.add_url_rule("/statii", view_func=StatiiView.as_view("statii"))
    app.db = connect()
    return app
