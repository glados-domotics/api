from glados import ma
from glados.models import Room


class RoomSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        # Make Scheme.dump() output an OrderedDict
        ordered = True
