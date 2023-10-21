from glados.models import Entity


def get_entities(filters):
    query = Entity.query

    type = filters.get("type")
    name = filters.get("name")
    status = filters.get("status")
    
    if type:
        query = query.filter(Entity.type == type)
    if (name):
        query = query.filter(Entity.name == name)
    if (status):
        query = query.filter(Entity.status == status)

    return query
