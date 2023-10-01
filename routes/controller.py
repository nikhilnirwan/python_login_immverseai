
from distutils.log import debug
import json
from flask import Flask,jsonify, request
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from midlware.midleware import not_found
import jwt
import datetime

my_secret = 'KJGjkh8HKHK'

# generate token
def jwt_generate(data):
	user = {
		"_id":data['_id'],
		"email":data['email'],
		"exp":datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
	}
	token = jwt.encode( payload = user, key = my_secret, algorithm = 'HS256')
	return token

# veryfy jwt token
def verify_jwt(token):
	token = jwt.decode(token, my_secret, algorithms=["HS256"])
	return token


def add_user(mongo):
	data = request.json
	
	if data["name"] and data["email"] and data["password"] and request.method == 'POST':
		data["password"] = generate_password_hash(data["password"])
		id = mongo.db.user.insert(data)
		resp = jsonify('User added successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()

# def add_user(mongo):
# 	_json = request.json
# 	_name = _json['name']
# 	_email = _json['email']
# 	_password = _json['password']
# 	_username = _json['username']
# 	if _name and _email and _password and request.method == 'POST':
# 		_hashed_password = generate_password_hash(_password)
# 		id = mongo.db.user.insert({'name': _name, 'email': _email, 'password': _hashed_password,'username':_username})
# 		resp = jsonify('User added successfully!')
# 		resp.status_code = 200
# 		return resp
# 	else:
# 		return not_found()

def users_all(mongo):
	users = mongo.db.user.find()

	resp = dumps(users)
	return resp

def user_by_id(mongo,id):
	user = mongo.db.user.find_one({'_id': ObjectId(id)})
	resp = json.loads(dumps(user))
	return resp

def update_user(mongo):
	_json = request.json
	_id = _json['_id']
	_name = _json['name']
	_email = _json['email']
	_password = _json['password']
	_username = _json['username']	
	if _name and _email and _password and _id and request.method == 'PUT':
		_hashed_password = generate_password_hash(_password)
		mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': _name, 'email': _email, 'password': _hashed_password,'username':_username}})
		resp = jsonify('User updated successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()

def delete_user(mongo,id):
	mongo.db.user.delete_one({'_id': ObjectId(id)})
	resp = jsonify('User deleted successfully!')
	resp.status_code = 200
	return resp

def login_user(mongo):
	result = request.json

	users = mongo.db.user.find({'email': result["email"]})

	userDetals = json.loads(dumps(users))
	# check password
	password = check_password_hash(userDetals[0]["password"], result["password"])
	print("password",password)

	if password : 
		userDetals[0]['token'] = jwt_generate(userDetals[0])
		return userDetals[0]
	else:
		message = "Your enterd password id wrong."
		return message