import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print("Connected fail with code", {rc})

client = mqtt.Client()
client.username_pw_set(username="dso_server", password="dso_password")
client.on_connect = on_connect
client.connect("35.198.179.56", 1883, 60)
client.loop_forever()