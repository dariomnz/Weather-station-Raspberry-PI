import requests
import os

def submit_device_info_to_store (data):
    host = os.getenv('DEVICES_MICROSERVICE_ADDRESS')
    port = os.getenv('DEVICES_MICROSERVICE_PORT')
    r = requests.post('http://' + host + ':' + port + '/devices/register', json=data)

def update_lat_long_time (data):
    host = os.getenv('DEVICES_MICROSERVICE_ADDRESS')
    port = os.getenv('DEVICES_MICROSERVICE_PORT')
    r = requests.post('http://' + host + ':' + port + '/devices/updater', json=data)
