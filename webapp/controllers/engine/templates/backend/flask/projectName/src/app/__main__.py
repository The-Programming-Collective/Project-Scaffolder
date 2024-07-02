from flask import Flask
from routes import api as api_blueprint

# Create the Flask app
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(api_blueprint, url_prefix="/api")

# Define the index route
@app.route("/")
def index():
  return "Hello, user test your routes by using /api/health"

if __name__ == "__main__":

  # Run the app
  app.run("localhost", 5000)
