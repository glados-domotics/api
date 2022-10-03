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


class EntityName(enum.IntEnum):
    Thermometer = 1
    Kitchen_light_1 = 2
    living_room_light_1 = 3
    living_room_light_2 = 4
    television = 5
    bedroom_switch_1 = 6
    bedroom_light_1 = 7
    Air_conditioner = 8