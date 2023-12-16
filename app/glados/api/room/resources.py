from flask import request, Response
from flask_restful import Resource

from glados.api.room.serializers import RoomSchema
import glados.repositories.rooms as repository


class RoomsAPI(Resource):
    def get(self):
        request_serializer = RoomSchema()
        params = request_serializer.load(request.args)

        entities = repository.filter(params)

        serializer = RoomSchema(many=True)
        return serializer.dump(entities), 200

    def post(self):
        request_serializer = RoomSchema()
        params = request_serializer.load(request.get_json())

        room = repository.add(params['name'])

        serializer = RoomSchema()
        return serializer.dump(room), 201


class RoomAPI(Resource):
    def get(self, id: str):
        room = repository.find(id)

        serializer = RoomSchema(many=False)
        return serializer.dump(room), 200

    def patch(self, id: str):
        request_serializer = RoomSchema()
        params = request_serializer.load(request.get_json())

        try:
            room = repository.update(id, params['name'])
        except ValueError:
            return Response(status=404)

        serializer = RoomSchema()
        return serializer.dump(room), 200
