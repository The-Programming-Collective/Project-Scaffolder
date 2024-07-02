# This is a sample route file
# it contains the functions and logic for the routes
# the api variable is the blueprint that is used to register the routes

from . import api

# Use annotations to define the endpoint that is going to appended to the prefix defined in the __main__.py file
@api.route('/health', methods=["GET"])
def health_check():
  return "App running nicely :)"

