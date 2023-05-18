import enum


class EntityType(enum.IntEnum):
    sensor = 1
    light = 2
    switch = 3
    multimedia = 4
    air_conditioner = 5


class EntityStatus(enum.IntEnum):
    on = 1
    off = 2
    unavailable = 3


class EntityRoom(enum.IntEnum):
    living_room = 1
    kitchen = 2
    bedroom = 3
    bathroom = 4
