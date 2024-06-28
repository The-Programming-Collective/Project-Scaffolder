# This is a sample route file
# it contains the blueprint that you will use to register the routes

from flask import Blueprint

health_blueprint = Blueprint("health", __name__, url_prefix="/health")

# Use annotations to define the endpoint that is going to appended to the prefix defined in the blueprint
@health_blueprint.route("/", methods=["GET"])
def health_check():
  return "App running nicely :)"
