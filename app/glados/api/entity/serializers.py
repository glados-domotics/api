from marshmallow import fields, validate, ValidationError

from glados import ma, constants
from glados.models import Entity, Room

from glados.api.room.serializers import RoomSerializer, RoomResponseSerializer

def validate_room_id_existance(room_id):
    if room_id is None:
        raise ValidationError("The room_id is None")
    if len(str(room_id)) != 36:
        raise ValidationError(f"The room_id length is incorrect; it should be 36 characters (UUID4 length). {len(str(room_id))} characters were provided")
    query = Room.query
    query = query.filter(Room.id == room_id)

def try_parse_float(s):
  try:
    return float(str(s))
  except ValueError:
    return None

def validate_value_possibilities(value):
    if try_parse_float(value) is not None:
        float_val = try_parse_float(value)
        if float_val > 256 or float_val < 0:
            raise ValidationError(f"The value should be between 0 and 255")
    else:
        if value not in constants.CHANNELS: raise ValidationError(f"The value '{value}' is not accepted.")

class EntitiesRequestSerializer(ma.Schema):
    type = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityType]))
    status = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityStatus]))
    room_id = fields.String(required=False, validate=validate_room_id_existance)


class EntitySerializer(ma.Schema):
    created_at = fields.DateTime("%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Entity
        include_relationships = True
        ordered = True
        fields = [
            "id",
            "name",
            "type",
            "status",
            "value",
            "room_id",
            "room",
            "created_at"
        ]
    room = ma.Nested(RoomSerializer)


class EntityResponseSerializer(EntitySerializer):
    pass


class EntityPatchRequestSerializer(ma.Schema):
    status = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityStatus]))
    value = fields.String(required=False, validate=validate_value_possibilities)
    # value = fields.String(required=False)  
