from gpiozero import DistanceSensor

sensor = DistanceSensor(echo=24, trigger=23)

def read_distance():   
    return int(sensor.distance * 100)


