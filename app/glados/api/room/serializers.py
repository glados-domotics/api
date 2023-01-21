from marshmallow import fields, validate, ValidationError

from glados import ma, constants
from glados.models import Room

class RoomSerializer(ma.Schema):
    created_at = fields.DateTime("%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Room
        ordered = True
        fields = [
            "id",
            "name",
            "created_at"
        ]

class RoomResponseSerializer(RoomSerializer):
    pass
