import paho.mqtt.client as mqtt
import tempSensor
import humiditySensor
import distanceSensor

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.publish("smart-heat", payload="hello from Pi", qos=1, retain=False)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("172.20.10.2", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#mqttc.loop_forever()
run = True
while run:
	rc = mqttc.loop(timeout=1.0)
	print(f"Furnace temperature: {tempSensor.read_temp()} C")
	print(f"Room temperature: {humiditySensor.read_temp()} C")
	print(f"Room humidity: {humiditySensor.read_humidity()}")
	print(f"Distance: {distanceSensor.read_distance()} cm")


	mqttc.publish("smart-heat/furnace-temp", payload=tempSensor.read_temp(), qos=1, retain=False)
	mqttc.publish("smart-heat/room-temp", payload=humiditySensor.read_temp(), qos=1, retain=False)
	mqttc.publish("smart-heat/room-humidity", payload=humiditySensor.read_humidity(), qos=1, retain=False)
	mqttc.publish("smart-heat/distance", payload=distanceSensor.read_distance(), qos=1, retain=False)



	if rc != 0:
		print("Error occured")

        # need to handle error, possible reconnecting or stopping the application

