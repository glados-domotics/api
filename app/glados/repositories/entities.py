from glados.models import Entity


def get_entities(filters):
    query = Entity.query

    type = filters.get("type")
    status = filters.get("status")
    if type:
        query = query.filter(Entity.type == type)
    if status:
        query = query.filter(Entity.status == status)

    return query
