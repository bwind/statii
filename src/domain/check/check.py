from marshmallow_oneofschema import OneOfSchema

from domain import OneOfSchemaMixin
from domain.check.http import HttpCheckSchema
from domain.check.ssh import SshCheckSchema


class CheckSchema(OneOfSchemaMixin, OneOfSchema):
    type_schemas = {"http": HttpCheckSchema, "ssh": SshCheckSchema}

    def get_obj_type(self, obj):
        obj_name = obj.__class__.__name__.replace("Check", "")
        return super().get_obj_type(obj=obj, obj_name=obj_name)
