import datetime
from dataclasses import dataclass

from marshmallow import Schema, fields, post_load

from domain import DateTimeField
from domain.check.base import BaseCheck
from domain.check.check import CheckSchema
from domain.status import Status, StatusSchema


@dataclass
class CheckStatus:
    check: BaseCheck
    timestamp: datetime.datetime
    status: Status


class CheckStatusSchema(Schema):
    check = fields.Nested(CheckSchema)
    timestamp = DateTimeField()
    status = fields.Nested(StatusSchema)

    @post_load
    def make_object(self, data, **kwargs):
        return CheckStatus(**data)
