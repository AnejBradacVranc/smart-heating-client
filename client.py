from db import MongoDBClient
from apscheduler.schedulers.background import BackgroundScheduler
from firebaseManager import FirebaseManager

import paho.mqtt.client as mqtt
import tempSensor
import humiditySensor
import distanceSensor
import dataProcessing
import cronService
import json
import time

class SensorDataState:
    current_distance = 0

state = SensorDataState()

firebase = FirebaseManager("/home/anejbv/certificates/smartheat-d8b87-firebase-adminsdk-fbsvc-0b545e50b8.json")

dbManager = MongoDBClient()
scheduler = BackgroundScheduler()
state.current_distance = 0

scheduler.add_job(cronService.notify_users, 'interval',[dbManager, firebase, state] ,minutes=10)

print("Starting cron service")
scheduler.start()


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("smart-heat/register-device", qos=2)


def on_message(client, userdata, msg):
	print(msg)
	try:
		print(msg.topic)
		if msg.topic == "smart-heat/register-device":	
			payload_str = msg.payload.decode('utf-8')
			data = json.loads(payload_str)		
			settings_update_resp = dbManager.update_one("settings", {"fuel_critical_point": data.get("fuelCriticalPoint")}, filter_query=None, upsert=True)
			if(settings_update_resp == None):
				print("ERROR: Could not save fuel critical level to db")
			else:
				print("Added critical fuel level to db", data.get("fuelCriticalPoint"))
			device_update_resp = dbManager.update("devices",{"token": data.get("token")}, {"token": data.get("token"), "timestamp": data.get("timestamp") })			
			if(device_update_resp == None):
				print("ERROR: Could not save device token to db")
			else:
				print("Added token to db", data.get("token"))
			print(msg.topic+" "+str(msg.payload))
	except Exception as e:
		print("Exception in on_message:", e)


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("192.168.1.148", 1883, 60)
mqttc.loop_start()
run = True
while run:
	try:
		furnaceTemp = tempSensor.read_temp()
		humidity = humiditySensor.read_humidity()
		roomTemp = humiditySensor.read_temp()
		distance = distanceSensor.read_distance()
		state.current_distance = distance		
		
		#print(f"Furnace temperature: {furnaceTemp} C")
		#print(f"Room temperature: {roomTemp} C")
		#print(f"Room humidity: {humidity}")
		#print(f"Distance: {distance} cm")		
		
		mqttc.publish("smart-heat/furnace-temp", payload=furnaceTemp, qos=1, retain=False)
		mqttc.publish("smart-heat/room-temp", payload=roomTemp, qos=1, retain=False)
		mqttc.publish("smart-heat/room-humidity", payload=humidity, qos=1, retain=False)
		mqttc.publish("smart-heat/distance",  payload=distance, qos=1, retain=False)
		#na neki moment za vse trenutno registrirane device sharni trenutni fuel level
		time.sleep(5)
			
	except Exception:
		print("Error occured with reading data")


