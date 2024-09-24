# DCS Mission Aircraft Editor (DCS-MAE)

## Introduction

This is a tool to help DCS Mission Editor's and Server Administrators easily edit mission data (in the form of a .lua file).
The tool will export all coalition's groups and their flights, allowing you to edit their data quickly and easily in either `json`, or `xlsx` format.

## Usage

### Creating an XLSX file from a lua file
1. `python lua_to_json.py --input <mission_file.miz> --output <output_file.json>`
2. `python json_to_xlsx.py --input <output_file.json> --output <excel_to_edit.xlsx>`

### Creating a JSON file from an XLSX file
1. `python xlsx_to_json.py --input <excel_to_edit.xlsx> --reference <output_file.json> --output <new_output_file.json>`
TODO: `python json_to_lua.py --input <new_output_file.json> --reference <mission_file.miz> --output <final_mission_output.miz>`

After this TODO step is done, the following can be deprecated:
### Creating a lua file from XLSX file
1. `python xlsx_to_csv --input [xlsx path] --output [output csv path]`
2. `python make_mission_lua.py --input <mission_file> --output <JSON file>`
3. `python csv_to_lua --csv <csv path> --out <output lua path> --json <json file path form step 2>`

> Please note that the `csv_to_lua` function is currently a work in progress and may not function properly at this time.

## Known issues
lua_to_csv.py path validation is broken if input file is not in current directory