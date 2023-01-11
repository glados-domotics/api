from marshmallow import fields, validate, ValidationError

from glados import ma, constants
from glados.models import Entity, Room

def validate_room_id_existance(room_id):
    if room_id is None:
        raise ValidationError("The room_id is None")
    if len(str(room_id)) != 36:
        raise ValidationError(f"The room_id length is incorrect; it should be 36 characters (UUID4 length). {len(str(room_id))} characters were provided")
    query = Room.query
    query = query.filter(Room.id == room_id)

class EntitiesRequestSerializer(ma.Schema):
    type = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityType]))
    status = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityStatus]))
    room_id = fields.String(required=False, validate=validate_room_id_existance)


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
            "room_id",
            "created_at"
        ]


class EntityResponseSerializer(EntitySerializer):
    pass
