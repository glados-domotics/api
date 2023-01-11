from glados.models import Entity


def get_entities(filters):
    query = Entity.query

    type = filters.get("type")
    status = filters.get("status")
    room_id = filters.get("room_id")
    if type:
        query = query.filter(Entity.type == type)
    if status:
        query = query.filter(Entity.status == status)
    if room_id:
        query = query.filter(Entity.room_id == room_id)
        print(query)

    return query
