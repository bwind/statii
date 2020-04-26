from domain.check import HTTPCheck, SSHCheck
from domain.rule import Rule
from domain.status import StatusEnum
from domain.test.less_than import LessThan


class CheckRepository:
    def find(self):
        return [
            HTTPCheck(
                url="https://api.maxwell.ai/2.0/health",
                check_status_code=200,
                check_response_text='{"success":true}\n',
            ),
            HTTPCheck(
                url="https://api.shopify.maxwell.ai/ping",
                check_status_code=200,
                check_response_text="OK",
            ),
            SSHCheck(
                hostname="api.shopify.maxwell.ai",
                username="maxwell",
                private_key=None,
                description="5 min loadavg < 0.25",
                command="cat /proc/loadavg | cut -d' ' -f2",
                rules=[
                    Rule(test=LessThan(0.1), status=StatusEnum.WARNING),
                    Rule(test=LessThan(0.3), status=StatusEnum.FAILED),
                ],
            ),
        ]
