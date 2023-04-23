from glados import ma
from glados.models import Room


class RoomSerializer(ma.Schema):

    class Meta:
        model = Room
        ordered = True
        fields = [
            "id",
            "name",
        ]
