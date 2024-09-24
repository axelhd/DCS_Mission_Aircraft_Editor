import luadata
import json
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
    default_output = os.path.join(os.getcwd(), "output", "output.json")
    parser = argparse.ArgumentParser(description="Convert DCS mission to JSON")

    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the .miz file to convert it to JSON",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=default_output,
        help="Output path for the JSON file",
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

def write_json(output, data):
    try:
        with open(output, mode="w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Data has been successfully exported to {output}")
    except Exception as e:
        raise IOError(f"Error writing to JSON file {output}: {e}")

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
    if not output.endswith(".json"):
        output += ".json"

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

    # Write the data to JSON
    write_json(output, data)

if __name__ == "__main__":
    main()
