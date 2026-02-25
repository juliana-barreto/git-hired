import os
from flask import Flask
from .database import db

# Create the GLOBAL Flask instance
app = Flask(__name__)

# Configure the database URI and other settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app immediately
db.init_app(app)

# Import models and routes at the VERY BOTTOM, ensuring 'app' and 'db' are already defined when routes tries to use them.
from . import models, routes

# Create tables once at startup
with app.app_context():
  db.create_all()