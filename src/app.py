import logging

import jinja2
import sentry_sdk
from flask import Flask

from config import settings

FORMAT = "* %(asctime)s - %(levelname)-8s * %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
logging.getLogger("pika").setLevel(logging.WARNING)


if settings.SENTRY_DSN:
    sentry_sdk.init(settings.SENTRY_DSN, environment=settings.ENVIRONMENT)


def create_app():
    app = Flask(__name__)
    app.jinja_loader = jinja2.ChoiceLoader(
        [app.jinja_loader, jinja2.FileSystemLoader(["web/templates"])]
    )
    return app
