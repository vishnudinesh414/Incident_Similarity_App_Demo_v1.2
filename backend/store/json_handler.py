# jason_handler.py

import json

def read_data(file_path):
    """Read JSON data from a file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def update_data(file_path, key, value):
    """Update a specific key in the JSON data."""
    data = read_data(file_path)
    data[key] = value
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)