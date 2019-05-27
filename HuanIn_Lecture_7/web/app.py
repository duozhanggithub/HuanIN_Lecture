from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
from sklearn import linear_model
import pickle

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.MLDatabase
users = db["Users"]

class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        hashed_pw =bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Results": ""
                    })

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for the API"
        }
        return jsonify(retJson)

def verifyPw(username, password):
    hashed_pw = users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'),hashed_pw) == hashed_pw:
        return True
    else:
        return False

class Store(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        inputs = postedData["inputs"]

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status": 302,
            }
            return jsonify(retJson)

        modelname = 'model.pkl'
        loaded_model = pickle.load(open(modelname, 'rb'), encoding='latin1')
        predcitions = loaded_model.predict([[float(inputs)]])

        users.update({
            "Username": username
        }, {
            "$set": {
                    "Results": float(predcitions)
                    }
        })

        retJson = {
            "status": 200,
            "msg": "inputs stores successfully"
        }

        return jsonify(retJson)

class Get(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status": 302,
            }
            return jsonify(retJson)

        results = users.find({
            "Username": username
        })[0]["Results"]

        retJson = {
            "status": 200,
            "results": str(results)
        }

        return jsonify(retJson)

api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')

if __name__=="__main__":
    app.run(host='0.0.0.0')
