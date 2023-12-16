from typing import Union
from uuid import UUID

from glados.models import Entity


def add(name: str, type: str, status: str, value: Union[int, None] = None, room_id: Union[UUID, None] = None):
    entity = Entity(
        name=name,
        type=type,
        status=status,
        value=value,
        room_id=room_id
    )
    entity.save(commit=True)

    return entity


def filter(filters: Union[dict, None] = None):
    """
    Return all or a filtered subset of entities. No checks for allowed filters are done here.
    """

    query = Entity.query
    if filters:
        for filter, value in filters.items():
            # TODO Is there a better syntax? Maybe with SQLAlchemy's API?
            query = query.filter(getattr(Entity, filter) == value)

    return query.all()


def find(id: str) -> Entity:
    entity = Entity.query.get(id)
    if entity:
        return entity
    else:
        raise ValueError("Entity not found")


def update(id: str, name: str, type: str, status: str, value: Union[int, None] = None, room_id: Union[UUID, None] = None):
    entity = Entity.query.get(id)
    if entity:
        entity.name = name
        entity.type = type
        entity.status = status
        entity.value = value
        entity.room_id = room_id
        entity.save(commit=True)

        return entity
    else:
        raise ValueError("Entity not found")
