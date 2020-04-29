from dataclasses import dataclass

from marshmallow import post_load

from domain.test.base import BaseTestSchema, Test


@dataclass
class EqualTo(Test):
    def test(self, value):
        return self.value == value


class EqualToSchema(BaseTestSchema):
    @post_load
    def make_object(self, data, **kwargs):
        return EqualTo(**data)
