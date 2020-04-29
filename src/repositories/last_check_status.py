import bson
from sticky_marshmallow import Repository

from domain.check_status import CheckStatusSchema


class LastCheckStatusRepository(Repository):
    class Meta:
        schema = CheckStatusSchema

    def save(self, obj):
        # make sure we only have a single CheckStatus for every check.
        existing_objs = self.find(check=bson.ObjectId(obj.check.id))
        if existing_objs.count() > 0:
            for existing_obj in existing_objs:
                self.delete(existing_obj)
        return super().save(obj)
