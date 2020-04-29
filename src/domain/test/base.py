from dataclasses import dataclass
from typing import Any

from marshmallow import Schema, fields


@dataclass
class Test:
    value: Any


class BaseTestSchema(Schema):
    value = fields.Raw()
