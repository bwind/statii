from marshmallow_oneofschema import OneOfSchema

from domain import OneOfSchemaMixin
from domain.test.equal_to import EqualToSchema
from domain.test.less_than import LessThanSchema


class TestSchema(OneOfSchemaMixin, OneOfSchema):
    type_schemas = {"less_than": LessThanSchema, "equal_to": EqualToSchema}
