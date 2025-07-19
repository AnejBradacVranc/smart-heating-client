from gpiozero import DistanceSensor
import os

echo_pin = int(os.getenv("DIST_ECHO", 24))
trigger_pin = int(os.getenv("DIST_TRIGGER", 23))

sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin)

def read_distance():   
    return int(sensor.distance * 100)


