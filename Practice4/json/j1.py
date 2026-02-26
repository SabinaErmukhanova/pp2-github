# Import built-in json module
# It allows us to work with JSON files in Python
import json

# STEP 1: Open JSON file

# "with open" opens the file safely
# "r" means read mode
# The file must be in the same folder as this script
with open("sample-data.json", "r") as file:
    
    # json.load() reads the file and converts JSON text
    # into a Python dictionary
    data = json.load(file)

# STEP 2: Print table header

print("Interface Status")

# Print long separator line
print("=" * 90)

# Print column names
# :60 means column width = 60 characters
# This keeps table aligned nicely
print(f"{'DN':60} {'Speed':10} {'MTU':6}")

print("-" * 90)

# STEP 3: Access JSON data

# In this JSON structure:
# data is a dictionary
# Inside it there is a key called "imdata"
# "imdata" contains a list of interface objects

for item in data["imdata"]:
    
    # Each item looks like:
    # {
    #   "l1PhysIf": {
    #       "attributes": { ... }
    #   }
    # }
    
    # So we go inside:
    # 1) l1PhysIf
    # 2) attributes
    
    attributes = item["l1PhysIf"]["attributes"]
    
    # STEP 4: Extract needed values

    # dn = Distinguished Name (full interface path)
    dn = attributes["dn"]
    
    # speed of interface
    speed = attributes["speed"]
    
    # MTU value
    mtu = attributes["mtu"]
    
    # STEP 5: Print formatted row

    # We format output so columns align properly
    print(f"{dn:60} {speed:10} {mtu:6}")