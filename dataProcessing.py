def calculate_remaining_fuel_percent(distance, critical_fuel_level):
    if critical_fuel_level == 0:
        return 0.0

    remaining = 1 - (distance / critical_fuel_level)
    return max(0.0, min(100.0, remaining * 100))
