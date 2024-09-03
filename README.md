# DCS Mission Aircraft Editor (DCS-MAE)

## Introduction

This is a tool to help DCS Mission Editor's and Server Administrators easily edit mission data (in the form of a .lua file).
The tool will export all coalition's groups and their flights, allowing you to edit their data quickly and easily in either `csv` or `xlsx` format.

## Usage

### Creating an XLSX file from a lua file
1. `python lua_to_csv.py --input <mission> --output <output>`
2. `python csv_to_xlsx.py --input [csv path] --output [output xlsx path]`

### Creating a lua file from XLSX file
1. `python xlsx_to_csv --input [xlsx path] --output [output csv path]`
2. `lua <output_file_from_step_1> --output <output>`
3. `python csv_to_lua --csv <csv path> --out <output lua path> --json <json file path form step 2>`

> Please note that the `csv_to_lua` function is currently a work in progress and may not function properly at this time.