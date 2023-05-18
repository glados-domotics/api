from glados.models import Entity, Room

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


def put_entity(new_entity):
    entity = Entity.query.get(new_entity["id"])
    new_room_id = Room.query.filter(Room.name == new_entity["room_name"]).first().id
    entity.room_id = new_room_id
    entity.name = new_entity["name"]
    entity.type = new_entity["type"]
    entity.status = new_entity["status"]
    # I don't new this ORM to be honest, but i have time to learn it
    return entity.save()
