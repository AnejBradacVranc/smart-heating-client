import paho.mqtt.client as mqtt
import tempSensor
import humiditySensor
import distanceSensor
from db import MongoDBClient

dbManager = MongoDBClient()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("smart-heat/register-device", qos=2)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	try:
		print(msg.topic)
		if msg.topic == "smart-heat/register-device":		
			resp = dbManager.update("firebaseDeviceTokens",{"token": str(msg.payload)}, {"token": str(msg.payload)})			
			if(resp == None):
				print("ERROR: Could not save device token to db")
			else:
				print("Added token to db", str(msg.payload))
			print(msg.topic+" "+str(msg.payload))
	except Exception as e:
		print("Exception in on_message:", e)


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("192.168.1.148", 1883, 60)

run = True
while run:
	try:
		furnaceTemp = tempSensor.read_temp()
		humidity = humiditySensor.read_humidity()
		roomTemp = humiditySensor.read_temp()
		distance = distanceSensor.read_distance()
		
		#print(f"Furnace temperature: {furnaceTemp} C")
		#print(f"Room temperature: {roomTemp} C")
		#print(f"Room humidity: {humidity}")
		#print(f"Distance: {distance} cm")		
		
		mqttc.publish("smart-heat/furnace-temp", payload=furnaceTemp, qos=1, retain=False)
		mqttc.publish("smart-heat/room-temp", payload=roomTemp, qos=1, retain=False)
		mqttc.publish("smart-heat/room-humidity", payload=humidity, qos=1, retain=False)
		mqttc.publish("smart-heat/distance", payload=distance, qos=1, retain=False)
		rc = mqttc.loop(timeout=2.0)

		if rc != 0:
			print("Error occured")
			
	except Exception:
		print("Error occured with reading data")


