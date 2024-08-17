import luadata
import csv
import sys


input = sys.argv[1]
output = sys.argv[2]

# Read the Lua data
data = luadata.read(input, encoding="utf-8")

# Open a CSV file for writing
with open(output, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the headers
    writer.writerow(
        ["Coalition", "Country", "Group Name", "Unit Name", "Unit Type", "X Coordinate", "Y Coordinate", "Task",
         "Skill", "Heading", "Fuel"])

    # Navigate through the data structure and extract relevant details
    for coalition, coalition_data in data["coalition"].items():
        for country in coalition_data["country"]:  # Directly iterate over the list
            country_name = country["name"]

            # Check if the country has any vehicles
            if "plane" in country:
                for group in country["plane"]["group"]:  # Directly iterate over the list
                    group_name = group["name"]
                    for unit in group["units"]:  # Directly iterate over the list
                        unit_name = unit["name"]
                        unit_type = unit["type"]
                        x_coord = unit["x"]
                        y_coord = unit["y"]
                        task = group.get("task", "N/A")
                        skill = unit["skill"]
                        heading = unit["heading"]
                        fuel = unit["payload"]["fuel"]

                        # Write the row to the CSV file
                        writer.writerow(
                            [coalition, country_name, group_name, unit_name, unit_type, x_coord, y_coord, task, skill,
                             heading, fuel])

print("Data has been successfully exported to mission_data.csv")
