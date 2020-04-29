from dataclasses import dataclass
from typing import List

from marshmallow import Schema, fields, post_load

from domain.check.base import BaseCheck
from domain.check.check import CheckSchema


@dataclass
class Service:
    title: str
    checks: List[BaseCheck]
    id: str = None


class ServiceSchema(Schema):
    id = fields.Str(allow_none=True)
    title = fields.Str()
    checks = fields.Nested(CheckSchema, many=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Service(**data)
