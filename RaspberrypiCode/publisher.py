import paho.mqtt.client as mqtt
import time
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
        send_state("Activo")
    else:
        print("Connected fail with code", {rc})

def on_disconnect(client, userdata, rc):
    print("Disconnected")

client = mqtt.Client()
def make_connection():
    client.username_pw_set(username="dso_server", password="dso_password")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect("35.198.162.23", 1883, 60)
    client.loop_forever()

def mqtt_disconnect():
    send_state("Inactivo")
    client.disconnect()

def send_temperature(temperature):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('/uc3m/classrooms/leganes/myclass/temperature', payload=temperature, qos=0, retain=False)
    time.sleep(1)


def send_humidity(humidity):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('/uc3m/classrooms/leganes/myclass/humidity', payload=humidity, qos=0, retain = False)
    time.sleep(1)

def send_latitude(latitude):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('/uc3m/classrooms/leganes/myclass/latitude', payload=latitude, qos=0, retain = False)
    time.sleep(1)

def send_longitude(longitude):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('/uc3m/classrooms/leganes/myclass/longitude', payload=longitude, qos=0, retain = False)
    time.sleep(1)

def send_id(id):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('/uc3m/classrooms/leganes/myclass/device_info', payload=id, qos=0, retain = False)
    time.sleep(1)

def send_state(state):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('/uc3m/classrooms/leganes/myclass/state', payload=state, qos=0, retain = False)
    time.sleep(1)
