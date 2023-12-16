from glados.models import Room


def add(name: str) -> Room:
    room = Room(name=name)
    room.save(commit=True)

    return room


def filter():
    """
    Return all the rooms
    """

    return Room.query.all()


def find(id: str) -> Room:
    room = Room.query.get(id)
    if room:
        return room
    else:
        raise ValueError("Room not found")


def update(id: str, name: str) -> Room:
    room = Room.query.get(id)
    if room:
        room.name = name
        room.save(commit=True)

        return room
    else:
        raise ValueError("Room not found")
