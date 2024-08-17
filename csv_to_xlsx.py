import pandas as pd
import argparse
import os


def main():
    default_input = os.path.join(os.getcwd(), "output", "output.csv")
    default_output = os.path.join(os.getcwd(), "output", "output.xlsx")
    parser = argparse.ArgumentParser(description="Convert CSV to XLSX")

    parser.add_argument(
        "--input",
        type=str,
        default=default_input,
        help="Path to the CSV file to convert to XLSX",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=default_output,
        help="Output path for the XLSX file",
    )

    args = parser.parse_args()

    # Ensure the output file has the correct extension
    output_file = args.output
    if not output_file.endswith(".xlsx"):
        output_file += ".xlsx"

    # Read the CSV file
    try:
        df = pd.read_csv(args.input, encoding="utf-8")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(
            f"File {args.input} is empty! Please provide a valid CSV file."
        )

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
