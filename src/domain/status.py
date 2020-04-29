from dataclasses import dataclass
from enum import Enum

from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField


class StatusEnum(Enum):
    UNKNOWN = "UNKNOWN"
    OK = "OK"
    WARNING = "WARNING"
    FAILED = "FAILED"

    def __gt__(self, other):
        order = [self.UNKNOWN, self.OK, self.WARNING, self.FAILED]
        return order.index(self) > order.index(other)


@dataclass
class Status:
    status: StatusEnum = StatusEnum.UNKNOWN
    message: str = None

    def __repr__(self):
        r = f"{self.__class__.__name__}: {self.status.name}"
        if self.message is not None:
            r += f" ({self.message})"
        return r


class StatusSchema(Schema):
    status = EnumField(StatusEnum)
    message = fields.Str()

    @post_load
    def make_object(self, data, **kwargs):
        return Status(**data)
