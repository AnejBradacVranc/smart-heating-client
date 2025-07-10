from gpiozero import DistanceSensor  # Import the DistanceSensor class from the gpiozero library

import tkinter as tk  # Import the tkinter library for creating the GUI

from tkinter import font  # Import the font module from tkinter for customizing the font

from time import sleep  # Import the sleep function from the time module for delay


# Initialize the ultrasonic sensor

sensor = DistanceSensor(echo=24, trigger=23, max_distance=5)

window = tk.Tk()
window.title("Distance Measurement")
custom_font = font.Font(size=30) 
window.geometry("800x400") 

distance_label = tk.Label(window, text="Distance: ", anchor='center', font=custom_font)

# Create a label to display the distance, centered text, and use the custom font

distance_label.pack()

def measure_distance():

   distance = int(sensor.distance * 100)  # Measure the distance and convert it to an integer

   distance_label.config(text="Distance: {} cm".format(distance))  # Update the distance label with the new distance


   window.after(1000, measure_distance)  # Schedule the next measurement after 1 second

def read_distance():   
   return int(sensor.distance * 100)
   


