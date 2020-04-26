from dataclasses import dataclass

from domain.test.test import Test


@dataclass
class EqualTo(Test):
    def test(self, value):
        return self.compare_value == value
