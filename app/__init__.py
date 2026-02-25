import os
from flask import Flask
from dotenv import load_dotenv
from .database import db

# Load environment variables from the .env file located in the root directory
load_dotenv()

def create_app():
    # Initialize the core Flask application
    app = Flask(__name__)

    # Retrieve database credentials from environment variables
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_name = os.getenv('DB_NAME', 'job_tracker')

    # Construct the SQLAlchemy database URI for MariaDB
    db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
    
    # Configure the Flask application
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Bind the database instance to this specific Flask application
    db.init_app(app)

    # Establish an application context to perform database setup operations
    with app.app_context():
        # Import models and enums locally to avoid circular dependency errors
        from . import enums
        from . import models
        
        # Automatically generate database tables based on defined models
        db.create_all()
        
        # Import and register route handlers
        from . import routes

    return app