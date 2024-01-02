from flask import request
from flask_restful import Resource

from glados.api.entity.serializers import EntitiesRequestSerializer, EntityResponseSerializer
from glados.repositories.entities import get_entities

from glados.api.entity.serializers import RoomSerializer, RoomResponseSerializer
from glados.repositories.room import get_rooms

from glados.models.room import Room
import uuid

from glados.api.entity.serializers import RoomBodySerializer

from glados.repositories.room import get_one_by_id

from glados.api.entity.serializers import EntityBodySerializer

from glados.models.entity import Entity

from glados.repositories.entities import get_one_entity_by_id


class EntitiesAPI(Resource):
    def get(self):
        request_serializer = EntitiesRequestSerializer()
        data = request_serializer.load(request.args)

        entities = get_entities(data)

        serializer = EntityResponseSerializer(many=True)
        return serializer.dump(entities), 200
    def post(self):
        request_serializer = EntityBodySerializer()
        data = request_serializer.load(request.json)
        entity = Entity(
            id=uuid.uuid4(),
            name=data.get("name"),
            type=data.get("type"),
            status=data.get("status"),
            value=data.get("value"),
            room_id=data.get("room")
        )
        entity.save(commit=True)
        return '', 201

class EntityById(Resource):
    def put(self, id):
        entity = get_one_entity_by_id(id)
        if entity == None:
            return '', 404

        request_serializer = EntityBodySerializer()
        data = request_serializer.load(request.json)

        entity.name = data.get("name")
        entity.type = data.get("type")
        entity.status = data.get("status")
        entity.value = data.get("value")
        entity.room_id = data.get("room")
        entity.save(commit=True)

        return '', 204

    def delete(self, id):
        entity = get_one_entity_by_id(id)
        if entity == None:
            return '', 404

        entity.remove(commit=True)
        return '', 204

class RoomAPI(Resource):
    def get(self):
        rooms = get_rooms()
        serializer = RoomResponseSerializer(many=True)
        return serializer.dump(rooms), 200
    def post(self):
        request_serializer = RoomBodySerializer()
        data = request_serializer.load(request.json)
        room = Room(id=uuid.uuid4(), name=data.get("name"))
        room.save(commit=True)

        return '', 201

class RoomAPIById(Resource):
    def put(self, id):
        room = get_one_by_id(id)
        if room == None:
            return '', 404

        request_serializer = RoomBodySerializer()
        data = request_serializer.load(request.json)

        room.name = data.get("name")
        room.save(commit=True)
        return '', 204
    def delete(self, id):
        room = get_one_by_id(id)
        if room == None:
            return '', 404

        room.remove(commit=True)
        return '', 204
