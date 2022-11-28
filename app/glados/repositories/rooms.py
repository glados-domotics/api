import uuid

from glados.models import Room


def get_rooms(filters) -> Room:
    query = Room.query

    if name := filters.get("name"):
        query = query.filter(Room.name == name)

    return query


def get_room(room_id) -> Room:
    return Room.query.filter_by(id=uuid.UUID(room_id).hex).first()
