from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__) # Create instance of Flask application
    CORS(app) 

    # Configure the database URI
    # replace postgres:// for SQLAlchemy compatability (Deprecated in later versions)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize app
    db.init_app(app)
    migrate = Migrate(app, db)

    # Import models and create them in the database
    with app.app_context():
        from . import models
        db.create_all()
    
    # Routes must be imported to make them available
    from .routes import register_routes
    register_routes(app)
    
    return app
