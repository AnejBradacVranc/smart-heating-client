import dataProcessing


def notify_users(dbManager, firebase, state):	
	devices = dbManager.find_all("devices")
	settings = dbManager.find_one("settings")
	if(settings is not None):
		for device in devices:
			remaining_fuel = dataProcessing.calculate_remaining_fuel_percent(state.current_distance, settings["fuel_critical_point"])
			print("Remaining fuel", remaining_fuel)
			print("Current distance", state.current_distance)

			if(remaining_fuel <0.1):
				firebase.send_to_token(
					token=device["token"],
					title="Low Fuel Alert",
					body="Your furnace is running low on fuel!.",
					channel_id="ch-1")
			else:
				print("Fuel level still sufficient", remaining_fuel)
	else:
		print("No settings yet initialized")
    
