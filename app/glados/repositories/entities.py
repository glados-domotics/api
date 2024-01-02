from glados.models import Entity
from sqlalchemy.orm.exc import NoResultFound


def get_entities(filters):
    query = Entity.query

    type = filters.get("type")
    if type:
        query = query.filter(Entity.type == type)

    status = filters.get("status")
    if status:
        query = query.filter(Entity.status == status)

    room = filters.get("room")
    if room:
        query = query.filter(Entity.room_id == room)

    return query
def get_one_entity_by_id(id):
    try:
        query = Entity.query
        return query.filter(Entity.id == id).one()
    except NoResultFound:
        return None
