from flask import Blueprint


# This is a sample route file
# it contains the blueprint that you will use to register the routes
# the api variable is the blueprint that will be used to register the routes
api = Blueprint("api", __name__)

from . import health
