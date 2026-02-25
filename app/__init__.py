import os
from flask import Flask
from dotenv import load_dotenv
from .database import db

# Load environment variables from the .env file located in the root directory
load_dotenv()

# Create the GLOBAL Flask instance
app = Flask(__name__)

# Configure the application 
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST', 'localhost')
db_name = os.getenv('DB_NAME', 'job_tracker')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app immediately
db.init_app(app)

# Import models and routes at the VERY BOTTOM, ensuring 'app' and 'db' are already defined when routes tries to use them.
from . import models, routes

# Create tables once at startup
with app.app_context():
  db.create_all()