import pandas as pd
import json
import os
import argparse

def extract_data_from_xlsx(input_file):
    # Read the Excel file
    df = pd.read_excel(input_file, sheet_name="Sheet1", header=None, skiprows=1)
    
    # Define the columns
    columns = [
        "Coalition", "Country", "Group Name", "Unit Name", "Unit Type",
        "X Coordinate", "Y Coordinate", "Task", "Skill", "Heading", "Fuel", "Loadouts"
    ]
    df.columns = columns

    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict(orient="records")
    
    return data

def update_json_structure(reference_data, extracted_data):
    # Update the reference JSON structure with the extracted data
    for row in extracted_data:
        coalition = row["Coalition"]
        country = row["Country"]
        group_name = row["Group Name"]
        unit_name = row["Unit Name"]
        unit_type = row["Unit Type"]
        x_coord = row["X Coordinate"]
        y_coord = row["Y Coordinate"]
        task = row["Task"]
        skill = row["Skill"]
        heading = row["Heading"]
        fuel = row["Fuel"]
        loadouts = eval(row["Loadouts"])  # Convert string representation of dict to actual dict

        if coalition not in reference_data["coalition"]:
            reference_data["coalition"][coalition] = {"country": []}
        
        country_list = reference_data["coalition"][coalition]["country"]
        country_data = next((c for c in country_list if c["name"] == country), None)
        if not country_data:
            country_data = {"name": country, "plane": {"group": []}}
            country_list.append(country_data)
        
        group_list = country_data["plane"]["group"]
        group_data = next((g for g in group_list if g["name"] == group_name), None)
        if not group_data:
            group_data = {"name": group_name, "units": []}
            group_list.append(group_data)
        
        unit_data = {
            "name": unit_name,
            "type": unit_type,
            "x": x_coord,
            "y": y_coord,
            "skill": skill,
            "heading": heading,
            "payload": {
                "fuel": fuel,
                "pylons": loadouts
            }
        }
        group_data["units"].append(unit_data)
    
    return reference_data

def main():
    default_output = os.path.join(os.getcwd(), "output", "output.json")
    parser = argparse.ArgumentParser(description="Convert XLSX to JSON using a reference JSON structure")

    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the XLSX file to convert to JSON",
    )

    parser.add_argument(
        "--reference",
        type=str,
        required=True,
        help="Path to the reference JSON file to maintain the structure",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=default_output,
        help="Output path for the JSON file",
    )

    args = parser.parse_args()

    # Ensure the input file path is absolute
    input_file = os.path.abspath(args.input)
    reference_file = os.path.abspath(args.reference)

    # Ensure the output file has the correct extension and is absolute
    output_file = args.output
    if not output_file.endswith(".json"):
        output_file += ".json"
    output_file = os.path.abspath(output_file)

    # Extract data from the XLSX file
    try:
        extracted_data = extract_data_from_xlsx(input_file)
    except Exception as e:
        raise ValueError(f"Error processing XLSX file {input_file}: {e}")

    # Read the reference JSON file
    try:
        with open(reference_file, 'r', encoding='utf-8') as f:
            reference_data = json.load(f)
    except Exception as e:
        raise ValueError(f"Error reading reference JSON file {reference_file}: {e}")

    # Update the reference JSON structure with the extracted data
    updated_data = update_json_structure(reference_data, extracted_data)

    # Write the updated data to JSON
    try:
        with open(output_file, mode="w", encoding="utf-8") as file:
            json.dump(updated_data, file, ensure_ascii=False, indent=4)
        print(f"Data has been successfully exported to {output_file}")
    except Exception as e:
        raise IOError(f"Error writing to JSON file {output_file}: {e}")

if __name__ == "__main__":
    main()