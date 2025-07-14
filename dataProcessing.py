import numpy as np

def calculate_remaining_fuel_percent(distance, critical_fuel_level):
    if critical_fuel_level == 0:
        return 0.0

    remaining = 1 - (distance / critical_fuel_level)
    return max(0.0, min(100.0, remaining * 100))
    
def calculate_remaining_fuel_percent_from_array(distances, critical_fuel_level, trim):
    try:
        critical_fuel_level = float(critical_fuel_level)
    except (ValueError, TypeError):
        return []

    if critical_fuel_level == 0 or not distances:
        return []

    values = np.array([entry["value"] for entry in distances])

    remaining = 1 - (values / critical_fuel_level)
    remaining_percent = np.clip(remaining * 100, 0.0, 100.0)

    if(not trim):
        return remaining_percent.tolist()
    else:
        try:
            trim = int(trim)
        except (ValueError, TypeError):
            return remaining_percent.tolist()
        return remaining_percent[-trim:].tolist()
    
def clean_array(array, trim = None):
   
    if not array:
        return []

    values = np.array([entry["value"] for entry in array])

    if(not trim):
        return values.tolist()
    else:
        try:
            trim = int(trim)
        except (ValueError, TypeError):
            return values.tolist()
        return values[-trim:].tolist()
   
