import logging
import uuid

from datetime import datetime

from glados import db
from glados.models import Entity, Room

logger = logging.getLogger(__name__)


def get_entity(id):
    return Entity.query.filter(Entity.id == id)

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

    return query.order_by('id')

def update_entity(id, filters):
    query = Entity.query.get(id)

    if filters.get("status"):
        query.status = "on"
    else:
        query.status = "off"
    query.name = filters.get("name") if filters.get("name", False) else query.name
    query.type = filters.get("type") if filters.get("type", False) else query.type
    query.value = filters.get("value") if filters.get("value", False) else query.value
    if filters.get('room'):
        room = Room.query.get(filters.get('room'))
        query.room_id = room.id

    if filters.get("created_at", False):
        new_date = datetime.strptime(filters.get("created_at"), '%d/%m/%y %H:%M:%S')
        query.created_at = new_date

    db.session.commit()
