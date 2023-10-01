
from flask import Flask,jsonify, request
from routes.controller import *
from db.db import mongos


app = Flask(__name__)

mongo = mongos(app)

@app.route('/register', methods=['POST'])
def add_users():
    return add_user(mongo)

@app.route('/users',methods=['GET'])
def user_find_all():
    return users_all(mongo)

@app.route('/user/<id>')
def single_user(id):
    return user_by_id(mongo,id)

@app.route('/update', methods=['PUT'])
def update_user_by_id():
    return update_user(mongo)

@app.route('/delete/<id>', methods=['DELETE'])
def delete_user_by_id(id):
    return delete_user(mongo,id)

@app.route('/login',methods=['POST'])
def login():
    return login_user(mongo)