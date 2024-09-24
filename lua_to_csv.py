import luadata
import csv
import os
import argparse
import zipfile
import tempfile

def validate_path(path):
    if not os.path.exists(path.rsplit('_', 1)[0]):
        print(path)
        raise FileNotFoundError(f"File {path.rsplit('_', 1)[0]} does not exist!")

def validate_output_path(path):
    """Ensure the directory for the output file exists, and create it if necessary."""
    save_path = os.path.join(os.getcwd(), path)
    directory = os.path.dirname(save_path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    elif os.path.isdir(save_path):
        raise ValueError(f"Output path {save_path} is a directory, not a file!")

def parse_arguments():
    default_output = os.path.join(os.getcwd(), "output", "output.csv")
    parser = argparse.ArgumentParser(description="Convert DCS mission to CSV")

    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the .miz file to convert it to CSV",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=default_output,
        help="Output path for the CSV file",
    )

    return parser.parse_args()

def extract_mission_file(_input, temp_dir):
    try:
        with zipfile.ZipFile(_input, 'r') as zip_ref:
            zip_ref.extract('mission', temp_dir)
    except zipfile.BadZipFile:
        raise ValueError(f"Error: {_input} is not a valid .miz file.")
    except KeyError:
        raise ValueError(f"Error: 'mission' file not found in {_input}.")
    except Exception as e:
        raise ValueError(f"Error extracting mission file from {_input}: {e}")

def read_lua_data(mission_file):
    try:
        return luadata.read(mission_file, encoding="utf-8")
    except Exception as e:
        raise ValueError(f"Error reading Lua file {mission_file}: {e}")

def write_csv(output, data):
    try:
        with open(output, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Write the headers
            writer.writerow(
                [
                    "Coalition",
                    "Country",
                    "Group Name",
                    "Unit Name",
                    "Unit Type",
                    "X Coordinate",
                    "Y Coordinate",
                    "Task",
                    "Skill",
                    "Heading",
                    "Fuel",
                    "Loadouts",
                ]
            )

            # Navigate through the data structure and extract relevant details
            for coalition, coalition_data in data.get("coalition", {}).items():
                for country in coalition_data.get("country", []):
                    country_name = country.get("name", "Unknown")

                    # Check if the country has any vehicles
                    if "plane" in country:
                        for group in country.get("plane", {}).get("group", []):
                            group_name = group.get("name", "Unknown")
                            for unit in group.get("units", []):
                                unit_name = unit.get("name", "Unknown")
                                unit_type = unit.get("type", "Unknown")
                                x_coord = unit.get("x", "Unknown")
                                y_coord = unit.get("y", "Unknown")
                                task = group.get("task", "N/A")
                                skill = unit.get("skill", "Unknown")
                                heading = unit.get("heading", "Unknown")
                                fuel = unit.get("payload", {}).get("fuel", "Unknown")
                                loadouts = unit.get("payload", {}).get("pylons", [])

                                # Convert loadouts to a string representation
                                loadouts_str = str(loadouts)

                                # Write the row to the CSV file
                                writer.writerow(
                                    [
                                        coalition,
                                        country_name,
                                        group_name,
                                        unit_name,
                                        unit_type,
                                        x_coord,
                                        y_coord,
                                        task,
                                        skill,
                                        heading,
                                        fuel,
                                        loadouts_str,
                                    ]
                                )

        print(f"Data has been successfully exported to {output}")
    except Exception as e:
        raise IOError(f"Error writing to CSV file {output}: {e}")

def main():
    args = parse_arguments()

    # variable name changed to avoid conflict with built-in input function
    _input = args.input
    output = args.output

    # Validate the input path
    try:
        validate_path(_input)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Please provide a valid input file path! | {_input} was not found."
        )

    # Ensure the output file has the correct extension
    if not output.endswith(".csv"):
        output += ".csv"

    # Validate the output path
    validate_output_path(output)

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract the mission file from the .miz archive
        extract_mission_file(_input, temp_dir)

        # Path to the extracted mission file
        mission_file = os.path.join(temp_dir, 'mission')

        # Read the Lua data
        data = read_lua_data(mission_file)

    # Write the data to CSV
    write_csv(output, data)

if __name__ == "__main__":
    main()
