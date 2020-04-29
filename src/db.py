import pymongo
from sticky_marshmallow import register_db

from config import settings


def connect():
    client = pymongo.MongoClient(
        host=settings.MONGODB_HOST.split(","), connect=False,
    )
    if settings.MONGODB_USERNAME and settings.MONGODB_PASSWORD:
        client[settings.MONGODB_DB].authenticate(
            settings.MONGODB_USERNAME, settings.MONGODB_PASSWORD
        )
    db = client[settings.MONGODB_DB]
    register_db(db)
    return db
