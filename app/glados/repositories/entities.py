from glados.models import Entity


def get_entities(filters):
    query = Entity.query

    type = filters.get("type")
    if type:
        query = query.filter(Entity.type == type)
    
    status = filters.get("status")
    if status:
        query = query.filter(Entity.status == status)
    
    name = filters.get("name")
    if name:
        query = query.filter(Entity.name == name)

    return query
