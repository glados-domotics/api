from marshmallow import fields, validate

from glados import ma, constants
from glados.models import Entity


class EntitiesRequestSerializer(ma.Schema):
    type = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityType]))
    status = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityStatus]))
    name = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityName]))

class EntitySerializer(ma.Schema):
    created_at = fields.DateTime("%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Entity
        ordered = True
        fields = [
            "id",
            "name",
            "type",
            "status",
            "value",
            "created_at"
        ]


class EntityResponseSerializer(EntitySerializer):
    pass
