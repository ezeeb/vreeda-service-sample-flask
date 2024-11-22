from dotenv import load_dotenv, dotenv_values
load_dotenv()

#config = dotenv_values(".env")
#print(".env:", config)

import os
from flask import Flask
from flask_cors import CORS
from libs.blueprint_loader import register_blueprints

app = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app)

from flask_pymongo import PyMongo

# MongoDB Konfiguration
app.config["MONGO_URI"] = os.getenv('MONGODB_URI')

try:
    # PyMongo-Instanz initialisieren
    mongo = PyMongo(app)
    db = mongo.cx.get_database()
    print(f"Successfully connected to database: {db.name}")
except Exception as e:
    print(f"MongoDB connection failed: {e}")

secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
app.secret_key = secret_key

# Register all blueprints
register_blueprints(app)