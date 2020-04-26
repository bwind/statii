from dataclasses import dataclass

from domain.status import StatusEnum
from domain.test.test import Test


@dataclass
class Rule:
    test: Test
    status: StatusEnum
