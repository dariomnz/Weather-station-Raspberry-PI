import Adafruit_DHT
from publisher import *
import uuid
import threading


import signal
import sys
import RPi.GPIO as GPIO

from Adafruit_CharLCD import Adafruit_CharLCD

# import gps
# import serial
import time
# import pynmea2
from pyembedded.gps_module.gps import GPS

import atexit

newhumidity = 0
newtemperature = 0
newlatitude = 0
newlongitude = 0

lcd = None
is_display_temp = True
is_sensor_error = False
n_error = 0

def weatherStation():
    DHT_SENSOR = Adafruit_DHT.DHT11
    DHT_PIN = 23

    global newtemperature,newhumidity,is_sensor_error
    while True:
        humidity,temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

        if humidity is not None and humidity < 100:
            if (newhumidity != humidity):
                newhumidity = humidity
                send_humidity(humidity)
                is_sensor_error = False
                update_pantalla()
            print("Hum={0:0.1f}% ".format(humidity))
        else:
            print("Sensore failure. Check wiring.")
            is_sensor_error = True
            update_pantalla()

        if temperature is not None and humidity < 100:
            if(newtemperature != temperature):
                newtemperature = temperature
                send_temperature(temperature)
                is_sensor_error = False
                update_pantalla()
            print("Temp={0:0.1f}C ".format(temperature))
        else:
            print("Sensore failure. Check wiring.")
            is_sensor_error = True
            update_pantalla()

        time.sleep(1)

def _publisher():
    make_connection()


def weatherSensor():
    id = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                   for ele in range(0,8*6,8)][::-1])
    print (id)
    send_id(id+" - Raspberry 1")

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_pressed_callback(channel):
    global is_display_temp
    is_display_temp = not is_display_temp
    update_pantalla()
    print("You've pressed the Button!")

def buttom():
    BUTTON_GPIO = 16
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING,
                          callback=button_pressed_callback, bouncetime=100)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

def setup_pantalla():
    global lcd
    lcd = Adafruit_CharLCD(rs=26, en=20,d4=19, d5=13, d6=6, d7=5,cols=16, lines=2)
    lcd.clear()
    lcd.message(' Weather station\n  Raspberry Pi')

def update_pantalla():
    global is_display_temp,is_sensor_error,n_error,lcd
    lcd.clear()
    if is_sensor_error:
        n_error += 1
        if n_error > 40:
            lcd.message("Sensore failure\nCheck wiring".format(newtemperature))
        else:
            if is_display_temp:
                lcd.message("  Temperatura  \n     {0:0.1f}C ".format(newtemperature))
            else:
                lcd.message("    Humedad    \n     {0:0.1f}% ".format(newhumidity))
    else:
        n_error = 0
        if is_display_temp:
            lcd.message("  Temperatura  \n     {0:0.1f}C ".format(newtemperature))
        else:
            lcd.message("    Humedad    \n     {0:0.1f}% ".format(newhumidity))

def gps():
    gps = GPS(port='/dev/ttyAMA0', baud_rate=9600)
    global newlatitude,newlongitude
    while True:
        try:
            values = gps.get_lat_long()
            raw_data = gps.get_raw_data()
            if values is not None and values[0] != 'N/A' and values[1] != 'N/A':
                latitude, longitude = values
                if raw_data[3] == "S":
                    latitude = - latitude;
                if raw_data[5] == "W":
                    longitude = - longitude;
                if (newlatitude != latitude):
                    newlatitude = latitude
                    send_latitude(latitude)

                if (newlongitude != longitude):
                    newlongitude = longitude
                    send_longitude(longitude)

                print("Lat={0:0.11f}".format(latitude))
                print("Long={0:0.11f}".format(longitude))
        except:
            print("GPS failure.")
        time.sleep(10)


if __name__ == "__main__":

    try:
    # atexit.register(mqtt_disconnect)
        publisher_thread = threading.Thread(target=_publisher)
        publisher_thread.start()
        time.sleep(1)

        weatherSensor()

        setup_pantalla()
        update_pantalla()

        weatherStation_thread = threading.Thread(target=weatherStation)
        weatherStation_thread.start()
        gps_thread = threading.Thread(target=gps)
        gps_thread.start()

        buttom()
    except:
        mqtt_disconnect()
        exit()
