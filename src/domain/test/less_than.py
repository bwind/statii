from dataclasses import dataclass

from domain.test.test import Test


@dataclass
class LessThan(Test):
    def test(self, value):
        if isinstance(self.value, float):
            test_value = float(value)
        elif isinstance(self.value, int):
            test_value = int(value)
        return test_value < self.value
