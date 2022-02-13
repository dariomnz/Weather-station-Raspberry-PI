import os
from flask import Flask, request
from flask_cors import CORS
from measurements_manager import *

app = Flask(__name__)
CORS(app)

@app.route('/measurements/register/', methods=['POST'])
def set_measurement():
    params = request.get_json()
    measurements_register(params)
    return {"result":"record inserted"}, 201

@app.route('/measurements/retrieve/')
def get_measurements():
    return measurements_retriever()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
app.run(host=HOST, port=PORT)
