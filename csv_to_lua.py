import luadata
import csv as csv_module
import json
from collections import defaultdict
import argparse

parser = argparse.ArgumentParser(description="Convert CSV to Lua")

parser.add_argument(
    "--csv_file",
    type=str,
    required=True,
    help="Path to the CSV file",
)

parser.add_argument(
    "--mission_file",
    type=str,
    required=True,
    help="Path to the mission file",
)

parser.add_argument(
    "--output_file",
    type=str,
    required=True,
    help="Path for the mission output file",
)

args = parser.parse_args()

csv_file = args.csv_file
mission = args.mission_file
output = args.output_file

# Read the CSV file and parse the data
data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
    reader = csv_module.DictReader(file)

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
        data[coalition][country]["plane"]["group"].append(
            {
                "name": group_name,
                "units": [
                    {
                        "name": unit_name,
                        "type": unit_type,
                        "x": x_coord,
                        "y": y_coord,
                        "skill": skill,
                        "heading": heading,
                        "payload": {"fuel": fuel},
                    }
                ],
                "task": task,
            }
        )

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
            (
                item
                for item in lua_data["coalition"][coalition]["country"]
                if item["name"] == country
            ),
            None,
        )

        if not country_entry:
            country_entry = {"name": country, "plane": {"group": []}}
            lua_data["coalition"][coalition]["country"].append(country_entry)

        for group_data in country_data["plane"]["group"]:
            group_name = group_data["name"]
            existing_group = next(
                (g for g in country_entry["plane"]["group"] if g["name"] == group_name),
                None,
            )

            if not existing_group:
                existing_group = {
                    "name": group_name,
                    "units": [],
                    "task": group_data["task"],
                }
                country_entry["plane"]["group"].append(existing_group)

            for unit in group_data["units"]:
                existing_group["units"].append(unit)

# write json to file for debugging
if True:
    with open("output.json", mode="w", encoding="utf-8") as file:
        json.dump(lua_data, file, indent=4, ensure_ascii=False)

# Write the updated Lua data back to the Lua file

with open(output, mode="w", encoding="utf-8") as file:
    file.write("mission = ")
    # Try saving as JSON for debugging
    json.dump(lua_data, file, indent=4, ensure_ascii=False)

print(f"Data has been successfully updated in {output}")
