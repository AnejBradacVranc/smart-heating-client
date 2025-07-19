import adafruit_dht
import board
import os

dht_pin_number = int(os.getenv("DHT_PIN", 12)) 

try:
    dht_board_pin = getattr(board, f"D{dht_pin_number}")
except AttributeError:
    raise ValueError(f"Invalid DHT_PIN: D{dht_pin_number} is not a valid board pin")

dht_device = adafruit_dht.DHT22(dht_board_pin)
	
def read_temp():
	return dht_device.temperature
	
def read_humidity(): 
	return dht_device.humidity

