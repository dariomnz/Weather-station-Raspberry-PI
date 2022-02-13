import mysql.connector
import os
import json

def connect_database ():
    mydb = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user =os.getenv('DBUSER'),
        password =os.getenv('DBPASSWORD'),
        database =os.getenv('DBDATABASE')
    )
    return mydb

def devices_retriever():
    mydb = connect_database()
    r = []
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT device_id, time, latitude, longitude, state FROM devices ORDER BY id DESC;")
        myresult = mycursor.fetchall()
        for device_id, time, latitude, longitude,state in myresult:
            r.append({"device_id": device_id, "time": time, "latitude": latitude, "longitude": longitude,"state": state})
        mydb.commit()
    result = json.dumps(r, sort_keys=True)
    return result

def devices_regiter(params):
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        sql = "INSERT INTO devices (device_id, time, latitude, longitude,state) VALUES (%s, %s, %s ,%s,%s)"
        val = (params["device_id"], params["time"], params["latitude"], params["longitude"],params["state"])
        device_id = (val,)
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except:
            print("Error inserting the device")
def devices_updater(params):
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        sql = "UPDATE devices SET time = %s,latitude = %s, longitude = %s, state = %s WHERE device_id = %s"
        val = (params["time"], params["latitude"], params["longitude"],params["state"],params["device_id"])
        device_id = (val,)
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record updated.")
        except:
            print("Error updating the device")
