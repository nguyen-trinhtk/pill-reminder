from flask import Flask
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)

    # MongoDB setup (use environment variable or config in real setup)
    client = MongoClient("your_mongo_uri")
    app.db = client['pill_dispenser']

    # Import and register routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
