import mysql.connector
import os
import json
import datetime

def connect_database ():
    mydb = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user=os.getenv('DBUSER'),
        password=os.getenv('DBPASSWORD'),
        database=os.getenv('DBDATABASE')
    )
    return mydb

def measurements_retriever():
    mydb = connect_database()
    r = []
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT temperature, humidity, time, latitude, longitude, device_id FROM sensor_data ORDER BY id DESC;")
        myresult = mycursor.fetchall()
        for temperature, humidity, time, latitude, longitude, device_id in myresult:
            r.append({"temperature": temperature, "humidity": humidity, "time": time, "latitude": latitude, "longitude": longitude, "device_id": device_id})
        mydb.commit()
    result = json.dumps(r, sort_keys=True)
    return result

def measurements_register(params):
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        sql = "INSERT INTO sensor_data (temperature, humidity, time, latitude, longitude, device_id) VALUES (%s, %s, %s ,%s ,%s, %s)"
        val = (params["temperature"], params["humidity"], params["time"], params["latitude"], params["longitude"], params["device_id"])
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except:
            print("Error inserting the measurements")
