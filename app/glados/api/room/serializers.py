from typing import Optional

from marshmallow import fields

from glados import ma
from glados.api.entity.serializers import EntityResponseSerializer
from glados.models import Room


class RoomsRequestSerializer(ma.Schema):
    name = fields.String(required=False)


class RoomSerializer(ma.Schema):
    created_at = fields.DateTime("%Y-%m-%dT%H:%M:%S")
    updated_at = fields.DateTime("%Y-%m-%dT%H:%M:%S")
    room_entities = fields.Method("get_room_entities")

    @staticmethod
    def get_room_entities(obj: Room) -> Optional[str]:
        serializer = EntityResponseSerializer(many=True)
        return serializer.dump(obj.entities)

    class Meta:
        model = Room
        ordered = True
        fields = [
            "id",
            "name",
            "room_entities",
            "created_at",
            "updated_at",
        ]


class RoomResponseSerializer(RoomSerializer):
    pass
