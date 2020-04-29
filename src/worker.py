#!/usr/bin/env python
import asyncio
import sys

from colored import attr, fg

from db import connect
from domain.status import StatusEnum
from logger import logging
from repositories.check import CheckRepository

# import sentry_sdk


# if settings.SENTRY_DSN:
#     sentry_sdk.init(settings.SENTRY_DSN, environment=settings.ENVIRONMENT)

INTERVAL = 30

COLORS = {
    StatusEnum.UNKNOWN: fg("blue"),
    StatusEnum.OK: fg("green"),
    StatusEnum.WARNING: fg(3) + attr("bold"),
    StatusEnum.FAILED: fg(1) + attr("bold"),
}
COLOR_RESET = attr("reset")


async def run_check(check):
    status = await check.run()
    message = status.status.name
    if status.message:
        message += f" {status.message}"
    logging.info(
        f"{check.__class__.__name__} {check.description}: {COLORS[status.status]}{message}{COLOR_RESET}"  # noqa: E501
    )


async def loop_forever():
    while True:
        checks = CheckRepository().find()
        coroutines = [run_check(check) for check in checks]
        coroutines.append(asyncio.sleep(INTERVAL))
        await asyncio.gather(*coroutines)


if __name__ == "__main__":
    logging.info("Starting worker...")
    connect()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop_forever())
    loop.close()
    logging.info("Worker exited.")
    sys.exit(1)
