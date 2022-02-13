import os
from flask import Flask, request
from flask_cors import CORS
from devices_manager import *

app = Flask(__name__)
CORS(app)

@app.route('/devices/register/', methods=['POST'])
def save_deviceinfo():
    params = request.get_json()
    devices_regiter(params)
    return {"result": "record inserted"}, 201

@app.route('/devices/updater/', methods=['POST'])
def update_deviceinfo():
    params = request.get_json()
    devices_updater(params)
    return {"result": "record updated"}, 201

@app.route('/devices/retrieve/')
def retrieve_devices():
    return devices_retriever()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
app.run(host=HOST, port=PORT)
