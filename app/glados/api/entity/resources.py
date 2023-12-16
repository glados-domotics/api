from flask import request, Response
from flask_restful import Resource

from glados.api.entity.serializers import EntitySchema
import glados.repositories.entities as repository


class EntitiesAPI(Resource):
    def get(self):
        request_serializer = EntitySchema()
        params = request_serializer.load(request.args, partial=True)

        entities = repository.filter(params)

        serializer = EntitySchema(many=True)
        return serializer.dump(entities), 200

    def post(self):
        request_serializer = EntitySchema()
        params = request_serializer.load(request.get_json())

        entity = repository.add(params['name'], params['type'], params['status'], params['value'], params['room_id'])

        serializer = EntitySchema()
        return serializer.dump(entity), 201


class EntityAPI(Resource):
    def get(self, id: str):
        entity = repository.find(id)

        serializer = EntitySchema(many=False)
        return serializer.dump(entity), 200

    def patch(self, id: str):
        request_serializer = EntitySchema()
        params = request_serializer.load(request.args)

        try:
            entity = repository.update(id, params['name'], params['type'], params['status'], params['value'], params['room_id'])
        except ValueError:
            return Response(status=404)

        serializer = EntitySchema()
        return serializer.dump(entity), 200
