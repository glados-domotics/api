from typing import Any, Tuple

from flask import request
from flask.views import MethodView

from glados import constants
from glados.api.entity.serializers import EntitiesRequestSerializer, EntityResponseSerializer
from glados.repositories.entities import get_entities, update_entity, get_entity


class EntitiesViews(MethodView):
    def get(self) -> Tuple[Any, int]:
        request_serializer = EntitiesRequestSerializer()
        filters = request_serializer.load(request.args)
        entities = get_entities(filters)
        serializer = EntityResponseSerializer(many=True)

        return serializer.dump(entities), 200


class EntityViews(MethodView):
    serializer = EntityResponseSerializer()

    def get(self, entity_id: str) -> Tuple[Any, int]:
        entity = get_entity(entity_id)

        return self.serializer.dump(entity), 200

    def put(self, entity_id: str) -> Tuple[Any, int]:
        data = EntityResponseSerializer().load(request.args)
        entity = update_entity(entity_id, data)

        return self.serializer.dump(entity), 200


class EntitiesFilterViews(MethodView):
    def get(self) -> Tuple[Any, int]:
        return [
            {
                "id": 1,
                "name": "Types",
                "choices": [
                    {"id": x.value, "name": x.name} for x in constants.EntityType
                ]
            },
            {
                "id": 2,
                "name": "Status",
                "choices": [
                    {"id": x.value, "name": x.name} for x in constants.EntityStatus
                ]
            },
        ], 200
