from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

def mongos(app):
    app.config["MONGO_URI"] = "mongodb://localhost:27017/pythonAPI"
    mongo = PyMongo(app)
    return mongo