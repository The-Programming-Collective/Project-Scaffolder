from flask import Flask
from app import routes

def main() -> Flask:
  app = Flask(__name__)

  return app

def run():
  app = main()
  app.run("localhost", 5000)

  routes.register(app)


if __name__ == "__main__":
  run()
