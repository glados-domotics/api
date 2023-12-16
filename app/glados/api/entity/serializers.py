import marshmallow
from marshmallow_sqlalchemy import auto_field

from glados import ma, constants
from glados.models import Entity


class EntitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Entity
        include_fk = True
        # Make Scheme.dump() output an OrderedDict
        ordered = True

    type = auto_field(validate=marshmallow.validate.OneOf([x.name for x in constants.EntityType]))
    status = auto_field(validate=marshmallow.validate.OneOf([x.name for x in constants.EntityStatus]))
