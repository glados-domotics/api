from marshmallow import fields, validate

from glados import ma, constants
from glados.models import Entity


class EntitiesRequestSerializer(ma.Schema):
    type = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityType]))
    room = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityRoom]))
    status = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityStatus]))
    id = fields.UUID(required=False)


class EntitySerializer(ma.Schema):
    created_at = fields.DateTime("%Y-%m-%dT%H:%M:%S")

    room_name = ma.Function(lambda obj: obj.room.name if obj.room else None)

    class Meta:
        model = Entity
        ordered = True
        include_fk = True
        fields = [
            "id",
            "name",
            "type",
            "status",
            "value",
            "created_at",
            "room_name"
        ]


class EntityResponseSerializer(EntitySerializer):
    pass
