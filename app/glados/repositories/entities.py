from glados.models import Entity
from glados import db
from sqlalchemy.orm import subqueryload


def get_entities(filters):
    query = Entity.query

    type = filters.get("type")
    status = filters.get("status")
    room_id = filters.get("room_id")

    # Better if it comes first
    if room_id:
        query = query.filter(Entity.room_id == room_id)
        print(query)
    if type:
        query = query.filter(Entity.type == type)
    if status:
        query = query.filter(Entity.status == status)

    return query


def get_entity(filters, entity_id):
    query = Entity.query
    query = query.options( subqueryload("room") ).get(entity_id)

    return query


def patch_entity(filters, entity_id):
    query = Entity.query
    query = query.get(entity_id)

    if query:
        if "value" in filters: query.value = float(filters["value"])
        if "status" in filters: query.status = filters["status"]
        db.session.commit()

    return query
