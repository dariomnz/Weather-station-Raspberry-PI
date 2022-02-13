from flask import Flask
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/dso/measurements/')
def get_sensor_data():
    measurements_microservice_server = os.getenv('MEASUREMENTS_MICROSERVICE_ADDRESS')
    measurements_microservice_port =  str(os.getenv('MEASUREMENTS_MICROSERVICE_PORT'))
    response = requests.get('http://' + measurements_microservice_server + ':' + measurements_microservice_port + '/measurements/retrieve/')
    return response.content

@app.route('/dso/devices/')
def get_device_list():
    devices_microservice_server = os.getenv('DEVICES_MICROSERVICE_ADDRESS')
    devices_microservice_port =  str(os.getenv('DEVICES_MICROSERVICE_PORT'))
    response = requests.get('http://' + devices_microservice_server + ':' + devices_microservice_port + '/devices/retrieve/')
    return response.content

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
app.run(host=HOST, port=PORT)
