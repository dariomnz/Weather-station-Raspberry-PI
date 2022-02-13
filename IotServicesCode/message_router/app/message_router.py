import paho.mqtt.client as paho
import os,time
from measurement_register_interface import *
from device_register_interface import *

# global vars definition
current_temperature=0
current_humidity=0
current_time=0
current_latitude=0
current_longitude=0
current_device=0
current_state="Inactivo"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
        client.subscribe("/uc3m/classrooms/leganes/myclass/temperature")
        client.subscribe("/uc3m/classrooms/leganes/myclass/humidity")
        client.subscribe("/uc3m/classrooms/leganes/myclass/latitude")
        client.subscribe("/uc3m/classrooms/leganes/myclass/longitude")
        client.subscribe("/uc3m/classrooms/leganes/myclass/device_info")
        client.subscribe("/uc3m/classrooms/leganes/myclass/state")
    else:
        print("Connected fail with code", {rc})


# define mqtt callback
def on_message(client, userdata, message):
    global current_temperature, current_humidity, current_time, current_latitude,current_longitude,current_device,current_state
    print("received message =",str(message.payload.decode("utf-8")))
    os.environ['TZ'] = 'Europe/Madrid'
    time.tzset()
    current_time = time.strftime('%a, %d %b %Y %H:%M:%S')
    # current_time = time.strftime('%d/%m/%Y %H:%M:%S')
    if message.topic == "/uc3m/classrooms/leganes/myclass/temperature":
        current_temperature = float(message.payload.decode("utf-8"))
        # datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data = {"temperature": current_temperature, "humidity": current_humidity, "time": current_time, "latitude": current_latitude, "longitude": current_longitude,"device_id": current_device,"state":current_state}
        submit_data_to_store(data)
        update_lat_long_time(data)
        print(data)
    if message.topic == "/uc3m/classrooms/leganes/myclass/humidity":
        current_humidity = float(message.payload.decode("utf-8"))
        # current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data = {"temperature": current_temperature, "humidity": current_humidity, "time": current_time, "latitude": current_latitude, "longitude": current_longitude,"device_id": current_device,"state":current_state}
        submit_data_to_store(data)
        update_lat_long_time(data)
        print(data)
    if message.topic == "/uc3m/classrooms/leganes/myclass/latitude":
        current_latitude = float(message.payload.decode("utf-8"))
        # current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data = {"temperature": current_temperature, "humidity": current_humidity, "time": current_time,
                "latitude": current_latitude, "longitude": current_longitude, "device_id": current_device,"state":current_state}
        submit_data_to_store(data)
        update_lat_long_time(data)
        print(data)
    if message.topic == "/uc3m/classrooms/leganes/myclass/longitude":
        current_longitude = float(message.payload.decode("utf-8"))
        # current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data = {"temperature": current_temperature, "humidity": current_humidity, "time": current_time, "latitude": current_latitude, "longitude": current_longitude,"device_id": current_device,"state":current_state}
        submit_data_to_store(data)
        update_lat_long_time(data)
        print(data)
    if message.topic == "/uc3m/classrooms/leganes/myclass/device_info":
        r = message.payload.decode("utf-8")
        current_device = r
        # current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data = {"device_id": r, "time": current_time, "latitude": current_latitude, "longitude": current_longitude,"state":current_state}
        submit_device_info_to_store(data)
        print(data)
    if message.topic == "/uc3m/classrooms/leganes/myclass/state":
        current_state = message.payload.decode("utf-8")
        # current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data = {"temperature": current_temperature, "humidity": current_humidity, "time": current_time, "latitude": current_latitude, "longitude": current_longitude,"device_id": current_device,"state":current_state}
        update_lat_long_time(data)
        print(data)


# Create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
myhost = os.getenv('BROKER_ADDRESS')
myport = int(os.getenv('BROKER_PORT'))
myuser = os.getenv('BROKER_USER')
mypassword = os.getenv('BROKER_PWD')
mykeepalive = int(os.getenv('BROKER_KEEP_ALIVE'))

client=paho.Client()
client.username_pw_set(username=myuser, password=mypassword)
client.on_connect = on_connect
# Bind function to callback
client.on_message=on_message
# Initializate cursor instance
print("connecting to broker ",myhost)
client.connect(myhost, 1883, mykeepalive) # connect
# Start loop to process received messages
client.loop_forever()