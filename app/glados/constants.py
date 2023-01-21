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


CHANNELS = ("TF1", "France2", "France3", "Arte", "France5", "M6")
