import datetime

import pytest

from domain.check.http import HttpCheck
from domain.check.ssh import SshCheck
from domain.check_status import CheckStatus
from domain.rule import Rule
from domain.service import Service
from domain.status import Status, StatusEnum
from domain.test.equal_to import EqualTo
from domain.test.less_than import LessThan
from web import app


@pytest.fixture()
def test_client():
    return app.test_client()


@pytest.fixture()
def http_check():
    return HttpCheck(
        description="App Health",
        url="https://app.maxwell.ai/",
        status_code_rules=[Rule(test=EqualTo(200), status=StatusEnum.FAILED)],
    )


@pytest.fixture()
def http_check_dump():
    return {
        "id": None,
        "description": "App Health",
        "type": "http",
        "timeout": 10.0,
        "url": "https://app.maxwell.ai/",
        "method": "GET",
        "status_code_rules": [
            {"test": {"type": "equal_to", "value": 200}, "status": "FAILED"}
        ],
        "response_text_rules": None,
    }


@pytest.fixture()
def ssh_check():
    return SshCheck(
        hostname="api.shopify.maxwell.ai",
        username="maxwell",
        private_key="private_key",
        description="load averages",
        command="cat /proc/loadavg | cut -d' ' -f2",
        stdout_rules=[
            Rule(test=LessThan(0.5), status=StatusEnum.WARNING),
            Rule(test=LessThan(1.0), status=StatusEnum.FAILED),
        ],
    )


@pytest.fixture()
def ssh_check_dump():
    return {
        "id": None,
        "description": "load averages",
        "hostname": "api.shopify.maxwell.ai",
        "command": "cat /proc/loadavg | cut -d' ' -f2",
        "username": "maxwell",
        "stdout_rules": [
            {"test": {"value": 0.5, "type": "less_than"}, "status": "WARNING"},
            {"test": {"value": 1.0, "type": "less_than"}, "status": "FAILED"},
        ],
        "private_key": {
            "ciphertext": b"\xb4\xc6\xd2\x89\xe5Y\xae\x8a<\xa0J",
            "nonce": b"E\xd0\xcb\xb9\xc2n\x9b7\x8d\xdcv\xa7\xd4\xbc\xa2\x9a",
            "tag": b"'\xd7 \xbcd5\t1\x17\xff\r\x06\x8d\x82v\x86",
        },
        "type": "ssh",
    }


@pytest.fixture()
def service(http_check):
    return Service(
        id="5ea972aaed4990e6c653aa59", title="API", checks=[http_check]
    )


@pytest.fixture()
def service_dump(http_check_dump):
    return {
        "id": "5ea972aaed4990e6c653aa59",
        "title": "API",
        "checks": [http_check_dump],
    }


@pytest.fixture()
def status_warning():
    return Status(
        status=StatusEnum.WARNING, message="Disk space critically low"
    )


@pytest.fixture()
def status_warning_dump():
    return {"status": "WARNING", "message": "Disk space critically low"}


@pytest.fixture()
def check_status(http_check, status_warning):
    return CheckStatus(
        check=http_check,
        timestamp=datetime.datetime(2020, 1, 7, 17, 12, 8, 937128),
        status=status_warning,
    )


@pytest.fixture()
def check_status_dump(http_check_dump, status_warning_dump):
    return {
        "check": http_check_dump,
        "timestamp": datetime.datetime(2020, 1, 7, 17, 12, 8, 937128),
        "status": status_warning_dump,
    }
