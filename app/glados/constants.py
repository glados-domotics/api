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

# class EntityName(enum.IntEnum):
#     Thermometer = 1
#     "Kitchen light 1" = 2
#     "Living room light 1" = 3
#     "Living room light 2" = 4
#     "Television" = 5
#     "Bedroom switch 1" = 6
#     "Bedroom light 1" = 7
#     "Air conditioner" = 8