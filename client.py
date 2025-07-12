import paho.mqtt.client as mqtt
import tempSensor
import humiditySensor
import distanceSensor
from db import MongoDBClient

dbManager = MongoDBClient()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.publish("smart-heat", payload="hello from Pi", qos=1, retain=False)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	if(msg.topic == "smart-heat/register-device"):		
		print(msg.topic+" "+str(msg.payload))

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("192.168.1.148", 1883, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#mqttc.loop_forever()
run = True
while run:
	try:
		furnaceTemp = tempSensor.read_temp()
		humidity = humiditySensor.read_humidity()
		roomTemp = humiditySensor.read_temp()
		distance = distanceSensor.read_distance()
		
		print(f"Furnace temperature: {furnaceTemp} C")
		print(f"Room temperature: {roomTemp} C")
		print(f"Room humidity: {humidity}")
		print(f"Distance: {distance} cm")
		
		
		mqttc.publish("smart-heat/furnace-temp", payload=furnaceTemp, qos=1, retain=False)
		mqttc.publish("smart-heat/room-temp", payload=roomTemp, qos=1, retain=False)
		mqttc.publish("smart-heat/room-humidity", payload=humidity, qos=1, retain=False)
		mqttc.publish("smart-heat/distance", payload=distance, qos=1, retain=False)
		rc = mqttc.loop(timeout=2.0)


		if rc != 0:
			print("Error occured")
			
	except Exception:
		print("Error occured with reading data")


