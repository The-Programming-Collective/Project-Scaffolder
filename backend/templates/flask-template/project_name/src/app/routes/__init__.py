from flask import Flask

# Add custom route files here
from .health import health_blueprint


# This function is used to register all custom routes
# to the main app as endpoints
def register(app: Flask) -> None:
  app.register_blueprint(health_blueprint)
