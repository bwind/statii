#!/usr/bin/env python
import asyncio
import sys

from logger import logging
from repositories.check import CheckRepository

# import sentry_sdk


# if settings.SENTRY_DSN:
#     sentry_sdk.init(settings.SENTRY_DSN, environment=settings.ENVIRONMENT)

INTERVAL = 30


async def run_check(check):
    status = await check.run()
    logging.info(f"{check}, {status}")


async def loop_forever():
    while True:
        checks = CheckRepository().find()
        coroutines = [run_check(check) for check in checks]
        await asyncio.gather(*coroutines)
        await asyncio.sleep(INTERVAL)


if __name__ == "__main__":
    logging.info("Starting worker...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop_forever())
    loop.close()
    logging.info("Worker exited.")
    sys.exit(1)
