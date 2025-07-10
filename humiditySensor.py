import adafruit_dht
import board
import tkinter as tk  # Import the tkinter library for creating the GUI

from tkinter import font  # Import the font module from tkinter for customizing the font

from time import sleep  # Import the sleep function from the time module for delay


window = tk.Tk()
window.title("Distance Measurement")
custom_font = font.Font(size=30) 
window.geometry("800x400") 

temperature_label = tk.Label(window, text="Distance: ", anchor='center', font=custom_font)
humidity_label = tk.Label(window, text="Distance: ", anchor='e', font=custom_font)


# Create a label to display the distance, centered text, and use the custom font

temperature_label.pack()
humidity_label.pack()

dht_device = adafruit_dht.DHT22(board.D12)


def measure_distance():
	temperature = dht_device.temperature
	humidity = dht_device.humidity

	temperature_label.config(text="Temperature: {} C".format(temperature))  # Update the distance label with the new distance
	humidity_label.config(text="Humidity: {}".format(humidity))  # Update the distance label with the new distance
	
	window.after(1000, measure_distance)  # Schedule the next measurement after 1 second
	
def read_temp():
	return dht_device.temperature
	
def read_humidity(): 
	return dht_device.humidity



#measure_distance()
#window.mainloop()

