from flask import jsonify
from flask.views import MethodView
from marshmallow import Schema, fields

from domain.status import StatusSchema
from repositories.service import ServiceRepository


class CheckAPIResponseSchema(Schema):
    id = fields.Str()
    description = fields.Str(allow_none=True)
    last_status = fields.Nested(StatusSchema)


class StatiiAPIResponseSchema(Schema):
    id = fields.Str()
    title = fields.Str()
    checks = fields.Nested(CheckAPIResponseSchema, many=True)


class StatiiView(MethodView):
    def get(self):
        services = ServiceRepository().find()
        return jsonify(
            services=StatiiAPIResponseSchema(many=True).dump(services)
        )
