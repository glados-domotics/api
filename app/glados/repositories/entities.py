from glados.models import Entity

ROOM_QUERY_TO_DB_MAPPER = {
    "living_room": "Living Room",
    "kitchen": "Kitchen",
    "bedroom": "Bedroom",
    "bathroom": "Bathroom"
}

def get_entities(filters):
    query = Entity.query
    type = filters.get("type")
    room = filters.get("room")
    status = filters.get("status")

    if type:
        query = query.filter(Entity.type == type)
    if room:
        query = query.filter(Entity.room.has(name=ROOM_QUERY_TO_DB_MAPPER[room]))
    if status:
        query = query.filter(Entity.status == status)

    return query
