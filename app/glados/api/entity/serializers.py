from typing import Optional

from marshmallow import fields, validate

from glados import ma, constants
from glados.models import Entity


class EntitiesRequestSerializer(ma.Schema):
    type = fields.String(
        required=False, validate=validate.OneOf([x.name for x in constants.EntityType])
    )
    room_id = fields.UUID(required=False)
    status = fields.String(
        required=False, validate=validate.OneOf([x.name for x in constants.EntityStatus])
    )


class EntityRequestSerializer(ma.Schema):
    name = fields.String(required=False)
    type = fields.String(
        required=False, validate=validate.OneOf([x.name for x in constants.EntityType])
    )
    room_id = fields.UUID(required=False)


class EntitySerializer(ma.Schema):
    created_at = fields.DateTime("%Y-%m-%dT%H:%M:%S")
    updated_at = fields.DateTime("%Y-%m-%dT%H:%M:%S")
    room_name = fields.Method("get_room_name")

    @staticmethod
    def get_room_name(obj: Entity) -> Optional[str]:
        return obj.room.name if obj.room else None

    class Meta:
        model = Entity
        ordered = True
        fields = [
            "id",
            "name",
            "type",
            "status",
            "value",
            "room_id",
            "room_name",
            "created_at",
            "updated_at"
        ]


class EntityResponseSerializer(EntitySerializer):
    pass
