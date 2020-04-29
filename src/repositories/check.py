from sticky_marshmallow import Repository

from domain.check.check import CheckSchema


class CheckRepository(Repository):
    class Meta:
        schema = CheckSchema
