import datetime
import re

from marshmallow import fields

from utils.crypto import decrypt, encrypt


class OneOfSchemaMixin:
    def get_obj_type(self, obj, obj_name=None):
        obj_name = obj_name or obj.__class__.__name__
        type_schema = (
            re.sub(r"([A-Z])", lambda m: f"_{m.group(1).lower()}", obj_name)
            .lower()
            .strip("_")
        )
        if type_schema not in self.type_schemas:
            raise Exception(f"Unknown object type: {type_schema}")
        return type_schema


class DateTimeField(fields.DateTime):
    # From https://github.com/marshmallow-code/marshmallow/issues/656
    def _deserialize(self, value, attr, data, partial):
        if isinstance(value, datetime.datetime):
            return value
        return super()._deserialize(value, attr, data)

    def _serialize(self, value, attr, obj):
        # Don't serialize. Retain datetime.datetime object as we're storing
        # this in MongoDB and we want ISODates, not strings.
        return value


class EncryptedStringField(fields.Field):
    default_error_messages = {"invalid": "Invalid slug"}
    SLUG_REGEX = r"^[a-z0-9]+[a-z0-9\-]*$"

    def _validated(self, value):
        if not isinstance(value, str):
            self.fail("invalid")
        return value

    def _serialize(self, value, attr, obj):
        encrypted_value = encrypt(value.encode())
        encrypted_dict = dict(
            zip(("ciphertext", "tag", "nonce"), encrypted_value)
        )
        return super()._serialize(encrypted_dict, attr, obj)

    def _deserialize(self, value, attr, data, partial):
        return decrypt(**value).decode()
