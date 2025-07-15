from flask import Flask, request, jsonify
from db import MongoDBClient
import json
import dataProcessing

app = Flask(__name__)
db = MongoDBClient()

@app.route('/')
def home():
    return "SmartHeat API is running!"

@app.route('/api/register-device', methods=['POST'])
def register_device():
    data = request.get_json()
    print("Registering device:", data)

    if (
        data.get("timestamp") is None or 
        data.get("fuel_critical_point") is None or 
        data.get("token") is None
    ):
        return jsonify({"success": False, "message": "Input data missing"})

    settings_update_resp = db.update_one(
        "settings",
        {"fuel_critical_point": data.get("fuel_critical_point")},
        filter_query=None,
        upsert=True
    )

    if settings_update_resp is None:
        print("ERROR: Could not save fuel critical level to DB")
        return jsonify({"success": False, "message": "ERROR: Could not save fuel critical level to DB"})
    else:
        print("Added critical fuel level to DB:", data.get("fuel_critical_point"))

    device_update_resp = db.update(
        "devices",
        {"token": data.get("token")},
        {"token": data.get("token"), "timestamp": data.get("timestamp")}
    )

    if device_update_resp is None:
        print("ERROR: Could not save device token to DB")
        return jsonify({"success": False, "message": "ERROR: Could not save device token to DB"})
    else:
        print("Added token to DB:", data.get("token"))

    return jsonify({"success": True})

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
        "room_humidity": dataProcessing.clean_array(humidity, trim),
		"fuel_percentage": dataProcessing.calculate_remaining_fuel_percent_from_array(distance, critical_fuel_level, trim)}, 
		default=str
		)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
