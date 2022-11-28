from typing import Any, Tuple

from flask import request
from flask.views import MethodView

from glados.api.room.serializers import RoomsRequestSerializer, RoomSerializer
from glados.repositories.rooms import get_rooms


class RoomsViews(MethodView):
    def get(self) -> Tuple[Any, int]:
        request_serializer = RoomsRequestSerializer()
        filters = request_serializer.load(request.args)
        rooms = get_rooms(filters)
        serializer = RoomSerializer(many=True)

        return serializer.dump(rooms), 200
