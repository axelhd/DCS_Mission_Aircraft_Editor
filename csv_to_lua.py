import sys
import luadata
from collections import defaultdict
import csv as csv_module
import json
import argparse

parser = argparse.ArgumentParser(description="Convert CSV to Lua")

parser.add_argument("--csv", type=str, required=True, help="Path to the CSV file")
parser.add_argument("--json", type=str, required=True, help="Path to the JSON file")
parser.add_argument("--out", type=str, required=True, help="Path for the mission output file")

args = parser.parse_args()

csv_file = args.csv
json_file = args.json
output = args.out


def save_json(data, out_file):
    try:
        with open(out_file, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Dictionary successfully written to {out_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


def csv_to_json(csv, out_file=None):
    csv_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
    with open(csv, mode="r", newline="", encoding="utf-8") as file:
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
            csv_data[coalition][country]["plane"]["group"].append(
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

    return csv_data


def json_file_to_dict(file_name):
    try:
        with open(file_name, 'r') as json_file:
            data_dict = json.load(json_file)
        return data_dict
    except FileNotFoundError:
        print(f"Error: The file {file_name} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {file_name} contains invalid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


def merge_dictionaries(dict1, dict2):
    merged_dict = dict1.copy()  # Start with dict1's keys and values

    for key, value in dict2.items():
        if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            merged_dict[key] = merge_dictionaries(merged_dict[key], value)
        else:
            # Otherwise, just overwrite or add the key-value pair
            merged_dict[key] = value

    return merged_dict


json_data = json_file_to_dict(json_file)
data = csv_to_json(csv_file)

merged = merge_dictionaries(json_data, data)

#save_json(merged, output)

luadata.write(output, merged, 'utf-8', indent="\t")
