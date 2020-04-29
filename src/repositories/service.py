from sticky_marshmallow import Repository

from domain.service import ServiceSchema


class ServiceRepository(Repository):
    class Meta:
        schema = ServiceSchema
