import json

class Planet:
    def __init__(self, name, temperature, cost_per_night, clothing_packages, available_rooms):
        self.name = name
        self.temperature = temperature
        self.cost_per_night = cost_per_night
        self.clothing_packages = clothing_packages
        self.available_rooms = available_rooms

# Load the data and create Planet instances
def load_planets(json_file="resort_information.json"):
    with open(json_file, "r") as file:
        data = json.load(file)
    
    planets = {}
    for planet_name, planet_info in data.items():
        planet = Planet(
            name=planet_name,
            temperature=planet_info["temperature"],
            cost_per_night=planet_info["cost_per_night"],
            clothing_packages=planet_info["clothing_packages"],
            available_rooms=planet_info["available_rooms"]
        )
        planets[planet_name] = planet
    return planets