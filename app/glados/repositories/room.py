from glados.models import Room
from sqlalchemy.orm.exc import NoResultFound

def get_rooms():
    query = Room.query
    return query

def get_one_by_id(id):
    try:
        query = Room.query
        return query.filter(Room.id == id).one()
    except NoResultFound:
        return None
