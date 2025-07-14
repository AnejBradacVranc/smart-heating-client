from flask import Flask, request
from db import MongoDBClient
import json
import dataProcessing

app = Flask(__name__)
db = MongoDBClient()

@app.route('/')
def home():
    return "SmartHeat API is running!"

@app.route('/api/history', methods=['GET'])
def get_latest_data():
	critical_fuel_level = request.args.get('critical_fuel_level')
	trim = request.args.get('trim') 
 
	
	if(not critical_fuel_level):
		critical_fuel_level = 100

	furnace_temp = db.find_all("furnace_temp")
	room_temp = db.find_all("room_temp")
	humidity = db.find_all("room_humidity")
	distance = db.find_all("distance")	

	return json.dumps({
        "furnace_temp": dataProcessing.clean_array(furnace_temp, trim),
        "room_temp": dataProcessing.clean_array(room_temp, trim),
        "humidity": dataProcessing.clean_array(humidity, trim),
		"fuel_percentage": dataProcessing.calculate_remaining_fuel_percent_from_array(distance, critical_fuel_level, trim)}, 
		default=str
		)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
