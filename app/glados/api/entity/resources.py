from flask import request
from flask_restful import Resource

from glados.api.entity.serializers import EntitiesRequestSerializer, EntityResponseSerializer, EntitiesPatchRequestSerializer
from glados.repositories.entities import get_entities, update_entity, get_entity


class EntitiesAPI(Resource):
    def get(self):
        request_serializer = EntitiesRequestSerializer()
        data = request_serializer.load(request.args)

        entities = get_entities(data)

        serializer = EntityResponseSerializer(many=True)
        return serializer.dump(entities), 200


class EntityAPI(Resource):
    def get(self, id):
        entity = get_entity(id)
        serializer = EntityResponseSerializer(many=True)
        return serializer.dump(entity), 200

    def patch(self, id):
        request_serializer = EntitiesPatchRequestSerializer()
        data = request_serializer.load(request.json)

        update_entity(id, data)
