import logging

from glados.models import Entity, Room

logger = logging.getLogger(__name__)


def get_entities(filters):
    query = Entity.query

    type = filters.get("type", False)
    status = filters.get("status", False)
    room = filters.get("room", False)

    if type:
        query = query.filter(Entity.type == type)
    if status:
        query = query.filter(Entity.status == status)
    if room:
        query = query.join(Room).filter(Room.name == room)

    return query
