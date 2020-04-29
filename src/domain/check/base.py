from dataclasses import dataclass

from marshmallow import Schema, fields

from domain.status import Status


class CheckFailedError(Exception):
    def __init__(self, status):
        self.status = status


@dataclass
class BaseCheck:
    id: str = None
    description: str = None

    def _run_rules(self, rules, value):
        """
        Ensures that the most severe status is raised.
        """
        if not rules:
            return
        status = None
        for rule in rules:
            if rule.test.test(value) is False:
                if status is None or rule.status > status:
                    status = rule.status
                    failed_rule = rule
        if status:
            raise CheckFailedError(
                status=Status(
                    status=status,
                    message=f"{repr(value)} does not pass {failed_rule.test}",
                )
            )


class BaseCheckSchema(Schema):
    id = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
