from flask import Flask, jsonify
from db import MongoDBClient

app = Flask(__name__)
db = MongoDBClient()

@app.route('/')
def home():
    return "SmartHeat API is running!"

@app.route('/history')
def get_latest_data():
    furnace_temp = db.get_latest("furnace_temp")
    room_temp = db.get_latest("room_temp")
    humidity = db.get_latest("room_humidity")
    distance = db.get_latest("distance")

    return jsonify({
        "furnace_temp": furnace_temp,
        "room_temp": room_temp,
        "humidity": humidity,
        "distance": distance
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
