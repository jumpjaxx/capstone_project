import json
import random


with open("resort_information.json", "r") as file:
    data = json.load(file)

# Randomize available_rooms for each planet
for planet in data:
    data[planet]["available_rooms"] = random.randint(1, 20)

# Save the updated data back to the file
with open("resort_information.json", "w") as file:
    json.dump(data, file, indent = 2)

print("Room availability updated!")