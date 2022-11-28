from flask import Blueprint
from flask_restful import Api

from glados.api.entity.resources import EntitiesViews, EntityViews, EntitiesFilterViews
from glados.api.misc import resources as misc_resources
from glados.api.room.resources import RoomsViews

blueprint = Blueprint("api", __name__)
api = Api(blueprint)

# Misc endpoints
api.add_resource(misc_resources.VersionAPI, "/")

# Entities endpoints
api.add_resource(EntitiesViews, "/entities")
api.add_resource(EntityViews, "/<string:entity_id>/entities")

# Filter endpoints
api.add_resource(EntitiesFilterViews, "/filters")

# Rooms endpoints
api.add_resource(RoomsViews, "/rooms")
