import asyncio
from dataclasses import dataclass
from typing import List

import aiohttp
from marshmallow import fields, post_load

from domain.check.base import BaseCheck, BaseCheckSchema, CheckFailedError
from domain.rule import Rule, RuleSchema
from domain.status import Status, StatusEnum


@dataclass
class BaseHttpCheck:
    url: str
    status_code_rules: List[Rule]
    response_text_rules: List[Rule] = None
    method: str = "GET"
    timeout: float = 10.0

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.url}"

    async def run(self):
        async with aiohttp.ClientSession() as client:
            method = getattr(client, self.method.lower())
            try:
                async with method(self.url, timeout=self.timeout) as response:
                    status_code = response.status
                    response_text = await response.text()
            except asyncio.TimeoutError:
                return Status(
                    StatusEnum.FAILED, message=f"Timeout after {self.timeout}s"
                )
            try:
                self._run_rules(self.status_code_rules, status_code)
                self._run_rules(self.response_text_rules, response_text)
            except CheckFailedError as exc:
                return exc.status
        return Status(status=StatusEnum.OK)


@dataclass
class HttpCheck(BaseCheck, BaseHttpCheck):
    pass


class HttpCheckSchema(BaseCheckSchema):
    url = fields.Str()
    status_code_rules = fields.Nested(RuleSchema, many=True)
    response_text_rules = fields.Nested(RuleSchema, many=True, allow_none=True)
    method = fields.Str()
    timeout = fields.Float()

    @post_load
    def make_object(self, data, **kwargs):
        return HttpCheck(**data)
