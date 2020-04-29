from dataclasses import dataclass

from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField

from domain.status import StatusEnum
from domain.test.base import Test
from domain.test.test import TestSchema


@dataclass
class Rule:
    test: Test
    status: StatusEnum


class RuleSchema(Schema):
    test = fields.Nested(TestSchema)
    status = EnumField(StatusEnum)

    @post_load
    def make_object(self, data, **kwargs):
        return Rule(**data)
