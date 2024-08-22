-- Load the dkjson library
local json = require("dkjson")

local input_file = nil
local output_file = nil

-- Parse the command-line arguments
for i = 1, #arg do
    if arg[i] == "--input" and arg[i+1] then
        input_file = arg[i+1]
    elseif arg[i] == "--output" and arg[i+1] then
        output_file = arg[i+1]
    end
end

-- Check if the required arguments were provided
if not input_file or not output_file then
    print("Usage: lua script.lua --input <input_file> --output <output_file>")
    os.exit(1)
end

-- Load the input file (assuming it's a Lua file returning a table)
local mission = dofile(input_file)

-- Example of a very nested Lua table
local nested_table = {
    key1 = {
        subkey1 = {
            subsubkey1 = "value1",
            subsubkey2 = {
                subsubsubkey1 = "value2",
                subsubsubkey2 = { "array_value1", "array_value2" }
            }
        },
        subkey2 = "value3"
    },
    key2 = "value4"
}

-- Convert the nested table to a JSON string
local json_string = json.encode(mission, { indent = true })

-- Write the JSON string to a file
local file = io.open(output_file, "w")
file:write(json_string)
file:close()

print("Nested table has been written to output.json")

