import luadata
import csv
import json
from collections import defaultdict
import sys

csv = sys.argv[1]
mission = sys.argv[2]
output = sys.argv[3]

# Read the CSV file and parse the data
data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

with open(csv, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        coalition = row["Coalition"]
        country = row["Country"]
        group_name = row["Group Name"]
        unit_name = row["Unit Name"]
        unit_type = row["Unit Type"]
        x_coord = float(row["X Coordinate"])
        y_coord = float(row["Y Coordinate"])
        task = row["Task"]
        skill = row["Skill"]
        heading = float(row["Heading"])
        fuel = float(row["Fuel"])

        # Structure the data to match the Lua format
        data[coalition][country]["plane"]["group"].append({
            "name": group_name,
            "units": [{
                "name": unit_name,
                "type": unit_type,
                "x": x_coord,
                "y": y_coord,
                "skill": skill,
                "heading": heading,
                "payload": {"fuel": fuel}
            }],
            "task": task
        })

# Load the existing Lua data
lua_data = luadata.read(mission, encoding="utf-8")

# Print Lua Data for Debugging
print("Loaded Lua Data:")
print(json.dumps(lua_data, indent=4))

# Update the Lua data with the new data
for coalition, coalition_data in data.items():
    if coalition not in lua_data["coalition"]:
        lua_data["coalition"][coalition] = {"country": []}

    for country, country_data in coalition_data.items():
        country_entry = next(
            (item for item in lua_data["coalition"][coalition]["country"] if item["name"] == country),
            None
        )

        if not country_entry:
            country_entry = {"name": country, "plane": {"group": []}}
            lua_data["coalition"][coalition]["country"].append(country_entry)

        for group_data in country_data["plane"]["group"]:
            group_name = group_data["name"]
            existing_group = next((g for g in country_entry["plane"]["group"] if g["name"] == group_name), None)

            if not existing_group:
                existing_group = {"name": group_name, "units": [], "task": group_data["task"]}
                country_entry["plane"]["group"].append(existing_group)

            for unit in group_data["units"]:
                existing_group["units"].append(unit)

# Print Updated Lua Data for Debugging
print("Updated Lua Data:")
print(json.dumps(lua_data, indent=4))

# Write the updated Lua data back to the Lua file

with open(output, mode='w', encoding='utf-8') as file:
    file.write("mission = ")
    # Try saving as JSON for debugging
    json.dump(lua_data, file, indent=4, ensure_ascii=False)

print(f"Data has been successfully updated in {output}")
