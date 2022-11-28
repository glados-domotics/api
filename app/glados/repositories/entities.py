import uuid

from glados.models import Entity, Room


def get_entities(filters):
    query = Entity.query

    if type := filters.get("type"):
        query = query.filter(Entity.type == type)

    if room_id := filters.get("room_id"):
        query = query.filter(Entity.room_id == room_id)

    if status := filters.get("status"):
        query = query.filter(Entity.status == status)

    return query


def get_entity(entity_id) -> Entity:
    return Entity.query.filter_by(id=uuid.UUID(entity_id).hex).first()


def update_entity(entity_id, data) -> Entity:
    entity: Entity = get_entity(entity_id)

    if name := data.get("name"):
        entity.name = name

    if type := data.get("type"):
        entity.type = type

    if room_id := data.get("room_id"):
        room = Room.query.filter(Room.id == room_id).first()
        entity.room = room

    entity.save()

    return entity
