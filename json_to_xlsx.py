import pandas as pd
import argparse
import os
import json

def extract_data(data):
    rows = []
    coalitions = data.get("coalition", {})
    for coalition_name, coalition_data in coalitions.items():
        countries = coalition_data.get("country", [])
        for country_data in countries:
            country_name = country_data.get("name", "")
            groups = country_data.get("plane", {}).get("group", [])
            for group in groups:
                group_name = group.get("name", "")
                units = group.get("units", [])
                for unit in units:
                    unit_name = unit.get("name", "")
                    unit_type = unit.get("type", "")
                    x_coord = unit.get("x", "")
                    y_coord = unit.get("y", "")
                    task = group.get("task", "")
                    skill = unit.get("skill", "")
                    heading = unit.get("heading", "")
                    fuel = unit.get("payload", {}).get("fuel", "")
                    loadouts = unit.get("payload", {}).get("pylons", {})
                    rows.append([
                        coalition_name, country_name, group_name, unit_name, unit_type,
                        x_coord, y_coord, task, skill, heading, fuel, str(loadouts)
                    ])
    return rows

def main():
    default_input = os.path.join(os.getcwd(), "output", "output.json")
    default_output = os.path.join(os.getcwd(), "output", "output.xlsx")
    parser = argparse.ArgumentParser(description="Convert JSON to XLSX")

    parser.add_argument(
        "--input",
        type=str,
        default=default_input,
        help="Path to the JSON file to convert to XLSX",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=default_output,
        help="Output path for the XLSX file",
    )

    args = parser.parse_args()

    # Ensure the input file path is absolute
    input_file = os.path.abspath(args.input)

    # Ensure the output file has the correct extension and is absolute
    output_file = args.output
    if not output_file.endswith(".xlsx"):
        output_file += ".xlsx"
    output_file = os.path.abspath(output_file)

    # Read the JSON file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract data and convert to DataFrame
        rows = extract_data(data)
        columns = [
            "Coalition", "Country", "Group Name", "Unit Name", "Unit Type",
            "X Coordinate", "Y Coordinate", "Task", "Skill", "Heading", "Fuel", "Loadouts"
        ]
        df = pd.DataFrame(rows, columns=columns)
    except ValueError as e:
        raise ValueError(f"File {input_file} is not a valid JSON file or is empty! Please provide a valid JSON file. Error: {e}")

    # Create and write to the Excel file
    try:
        with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
            # Convert the dataframe to an XlsxWriter Excel object.
            df.to_excel(
                writer, sheet_name="Sheet1", startrow=1, header=False, index=False
            )

            # Get the xlsxwriter workbook and worksheet objects.
            workbook = writer.book
            worksheet = writer.sheets["Sheet1"]

            # Get the dimensions of the dataframe.
            (max_row, max_col) = df.shape

            # Create a list of column headers, to use in add_table().
            column_settings = [{"header": header} for header in df.columns]

            # Add the table.
            worksheet.add_table(
                0, 0, max_row, max_col - 1, {"columns": column_settings}
            )

            # Make the columns wider for clarity.
            worksheet.set_column(0, max_col - 1, 12)
    except Exception as e:
        print(f"An error occurred while writing the Excel file: {e}")
        raise


if __name__ == "__main__":
    main()
