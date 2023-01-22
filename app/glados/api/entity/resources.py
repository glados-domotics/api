from flask import request
from flask_restful import Resource, abort
import os

from glados.api.entity.serializers import EntitiesRequestSerializer, EntityResponseSerializer, EntityPatchRequestSerializer
from glados.repositories.entities import get_entities, get_entity, patch_entity


class EntitiesAPI(Resource):
    def get(self):
        request_serializer = EntitiesRequestSerializer()
        data = request_serializer.load(request.args)

        entities = get_entities(data)

        serializer = EntityResponseSerializer(many=True)
        return serializer.dump(entities), 200

class EntityAPI(Resource):
    def get(self, entity_id):
        request_serializer = EntitiesRequestSerializer()
        data = request_serializer.load(request.args)

        entity = get_entity(data, entity_id)

        serializer = EntityResponseSerializer(many=False)
        result = serializer.dump(entity)
        if result is None or len(result) == 0:
            abort(404, message="Entity {} doesn't exist".format(entity_id))
        return result, 200

    def patch(self, entity_id):
        if not ('Authorization' in request.headers and request.headers['Authorization'][7:] == os.environ.get("BEARER_TOKEN")):
            abort(401, message="You're not authorized to perform this action. Bearer token requierd")
        request_serializer = EntityPatchRequestSerializer()
        data = request_serializer.load(request.form)


        entity = patch_entity(data, entity_id)

        serializer = EntityResponseSerializer(many=False)
        result = serializer.dump(entity)
        if result is None or len(result) == 0:
            abort(404, message="Entity {} doesn't exist".format(entity_id))
        return result, 200
