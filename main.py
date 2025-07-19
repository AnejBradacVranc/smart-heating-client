from db import MongoDBClient
from apscheduler.schedulers.background import BackgroundScheduler
from firebaseManager import FirebaseManager
from flask import Flask

import paho.mqtt.client as mqtt
import tempSensor
import humiditySensor
import distanceSensor
import dataProcessing
import cronService
import json
import time
import os


class SensorDataState:
    current_distance = 0


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def main():
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/home/anejbv/certificates/smartheat-d8b87-firebase-adminsdk-fbsvc-0b545e50b8.json")
    if not cred_path:
        raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS env var with Firebase key path")

    global dbManager

    state = SensorDataState()
    firebase = FirebaseManager(cred_path)
    dbManager = MongoDBClient()
    scheduler = BackgroundScheduler()
    state.current_distance = 0

    scheduler.add_job(cronService.notify_users, 'interval', [dbManager, firebase, state], minutes=1)
    print("Starting cron service")
    scheduler.start()

 
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    broker = os.getenv("MQTT_BROKER", "localhost")
    port = int(os.getenv("MQTT_PORT", 1883))
    mqttc.connect(broker, port, 60)
    mqttc.loop_start()
    last_insert = time.time()
    
    print("Broker running on address:", broker)
    print("and port", port)

    run = True
    while run:
        try:
            furnaceTemp = tempSensor.read_temp()
            humidity = humiditySensor.read_humidity()
            roomTemp = humiditySensor.read_temp()
            distance = distanceSensor.read_distance()
            state.current_distance = distance
            

            mqttc.publish("smart-heat/furnace-temp", payload=furnaceTemp, qos=1, retain=True)
            mqttc.publish("smart-heat/room-temp", payload=roomTemp, qos=1, retain=True)
            mqttc.publish("smart-heat/room-humidity", payload=humidity, qos=1, retain=True)
            mqttc.publish("smart-heat/distance", payload=distance, qos=1, retain=True)
            
            if time.time() - last_insert > 10:
                dbManager.insert("furnace_temp", {"value": furnaceTemp})
                dbManager.insert("room_temp", {"value": roomTemp})
                dbManager.insert("room_humidity", {"value": humidity})
                dbManager.insert("distance", {"value": distance})
                last_insert = time.time()

            time.sleep(2)

        except Exception:
            print("Error occurred with reading data")


if __name__ == '__main__':
    main()
