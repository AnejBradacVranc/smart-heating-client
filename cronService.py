import dataProcessing


def notify_users(dbManager, firebase, current_distance):
	#get users, 
	devices = dbManager.find_all("devices")
	settings = dbManager.find_one("settings")
	for device in devices:
		remaining_fuel = dataProcessing.calculate_remaining_fuel_percent(current_distance, settings["fuel_critical_point"])
		if(remaining_fuel <0.1):
			firebase.send_to_token(
                token=device["token"],
                title="Low Fuel Alert",
                body="Your furnace is running low on fuel!.")
			#notify through admin sdk
			  
    
