import luadata
import csv
import os
import argparse


def validate_path(path):
    if not os.path.exists(path.rsplit('_', 1)[0]):
        raise FileNotFoundError(f"File {path.rsplit('_', 1)[0]} does not exist!")


def validate_output_path(path):
    """Ensure the directory for the output file exists, and create it if necessary."""
    save_path = os.path.join(os.getcwd(), path)
    directory = os.path.dirname(save_path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    elif os.path.isdir(save_path):
        raise ValueError(f"Output path {save_path} is a directory, not a file!")


def main():
    default_output = os.path.join(os.getcwd(), "output", "output.csv")
    parser = argparse.ArgumentParser(description="Convert CSV to XLSX")

    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the CSV file to convert to XLSX",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=default_output,
        help="Output path for the XLSX file",
    )

    args = parser.parse_args()

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

    # Read the Lua data
    try:
        data = luadata.read(_input, encoding="utf-8")
    except Exception as e:
        raise ValueError(f"Error reading Lua file {_input}: {e}")

    # Open a CSV file for writing
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
                                    ]
                                )

        print(f"Data has been successfully exported to {output}")
    except Exception as e:
        raise IOError(f"Error writing to CSV file {output}: {e}")


if __name__ == "__main__":
    main()
