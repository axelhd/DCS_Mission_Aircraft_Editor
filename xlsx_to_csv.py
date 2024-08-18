import pandas as pd
from openpyxl import load_workbook
import os
import argparse


def validate_input_path(path):
    """Validate that the input path exists and is a file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} does not exist!")
    if not os.path.isfile(path):
        raise ValueError(f"Path {path} is not a file!")


def validate_output_path(path):
    """Ensure the directory for the output file exists, and create it if necessary."""
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    elif os.path.isdir(path):
        raise ValueError(f"Output path {path} is a directory, not a file!")


def convert_xlsx_to_csv(input_path, output_path):
    """Convert an Excel file to CSV."""
    wb = load_workbook(input_path)
    df = pd.DataFrame(wb.active.values)
    df.to_csv(output_path, index=False, header=False)
    print(f"Data has been successfully exported to {output_path}")


def main():
    default_input = os.path.join(os.getcwd(), "output", "output.xlsx")
    default_output = os.path.join(os.getcwd(), "output", "output.csv")
    parser = argparse.ArgumentParser(description="Convert an Excel file to CSV.")

    parser.add_argument(
        "--input",
        type=str,
        default=default_input,
        help="Path to the input Excel (.xlsx) file",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=default_output,
        help="Path to the output CSV file",
    )

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    # Validate the input and output paths
    try:
        validate_input_path(input_path)
    except (FileNotFoundError, ValueError) as e:
        raise e

    try:
        validate_output_path(output_path)
    except ValueError as e:
        raise e

    # Convert Excel to CSV
    try:
        convert_xlsx_to_csv(input_path, output_path)
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        raise


if __name__ == "__main__":
    main()
