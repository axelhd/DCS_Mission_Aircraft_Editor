import argparse
import os
from pathlib import Path
import subprocess

# Arg stuff
parser = argparse.ArgumentParser(description="Convert CSV to Lua")
parser.add_argument("--input", type=str, required=True, help="Path to the LUA file")
parser.add_argument("--output", type=str, required=True, help="Path to the output file")

args = parser.parse_args()
mission = args.input
output = args.output

# Append lua to mission
with open(mission, "a") as file:
    file.write("""
-- Load the dkjson library
local json = require("dkjson")

local output_file = nil

-- Parse the command-line arguments
for i = 1, #arg do
    if arg[i] == "--output" then
        output_file = arg[i+1]
    end
end
print(output_file)
-- Check if the required arguments were provided
if not output_file then
    print("Usage: lua mission.lua --output <output_file>")
    os.exit(1)
end

-- Convert the nested table to a JSON string
local json_string = json.encode(mission, { indent = true })

-- Write the JSON string to a file
local file = io.open(output_file, "w")
file:write(json_string)
file:close()

print("Nested table has been written to output file")

""")
    file.close()

# Add .lua extension
p = Path(mission)
p.rename(p.with_suffix('.lua'))
mission = f"{mission}.lua"

#subprocess.run(["lua", f"{mission}", "--output", output])
os.system(f"lua {mission} --output {output}")
print(f"lua {mission} --output {output}")
# Cleanup
with open(mission, "r+") as fp:
    lines = fp.readlines()
    fp.seek(0)
    fp.truncate()

    fp.writelines(lines[:-28])


