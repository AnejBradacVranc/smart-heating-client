import adafruit_dht
import board

dht_device = adafruit_dht.DHT22(board.D12)
	
def read_temp():
	return dht_device.temperature
	
def read_humidity(): 
	return dht_device.humidity

