from marshmallow import fields, validate

from glados import ma, constants
from glados.models import Entity

class RoomBodySerializer(ma.Schema):
    name = fields.String(required=True)

class RoomSerializer(ma.Schema):
    id = fields.String()
    name = fields.String()

class EntitiesRequestSerializer(ma.Schema):
    type = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityType]))
    status = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityStatus]))
    room = fields.UUID(required=False)

class EntityBodySerializer(ma.Schema):
    name = fields.String(required=True)
    value = fields.String(required=False)
    type = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityType]))
    status = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityStatus]))
    room = fields.UUID(required=False)

class EntitySerializer(ma.Schema):
    created_at = fields.DateTime("%Y-%m-%dT%H:%M:%S")
    room = fields.Nested(RoomSerializer)
    class Meta:
        model = Entity
        ordered = True
        fields = [
            "id",
            "name",
            "type",
            "status",
            "value",
            "created_at",
            "room",
        ]

class EntityResponseSerializer(EntitySerializer):
    pass
class RoomResponseSerializer(RoomSerializer):
    pass
