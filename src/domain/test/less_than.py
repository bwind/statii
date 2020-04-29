from dataclasses import dataclass

from marshmallow import post_load

from domain.test.base import BaseTestSchema, Test


@dataclass
class LessThan(Test):
    def test(self, value):
        if isinstance(self.value, float):
            test_value = float(value)
        elif isinstance(self.value, int):
            test_value = int(value)
        return test_value < self.value


class LessThanSchema(BaseTestSchema):
    @post_load
    def make_object(self, data, **kwargs):
        return LessThan(**data)
