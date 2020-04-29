import os
import sys

this = sys.modules[__name__]
env = os.environ

params = (
    "ENVIRONMENT",
    "MONGODB_DB",
    "MONGODB_HOST",
    "MONGODB_USERNAME",
    "MONGODB_PASSWORD",
    "SECRET_KEY",
    "SENTRY_DSN",
)

for param in params:
    setattr(this, param, env[param])

assert len(env["SECRET_KEY"]) == 32
