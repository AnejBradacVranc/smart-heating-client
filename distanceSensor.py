from gpiozero import DistanceSensor  # Import the DistanceSensor class from the gpiozero library

sensor = DistanceSensor(echo=24, trigger=23, max_distance=5)

def read_distance():   
   return int(sensor.distance * 100)
   


