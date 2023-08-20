# config_utils.py

import json
import os

def load_config(filename='config.json'):
    """Load configuration from a JSON file."""

    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_script_directory))
    config_path = os.path.join(project_root, filename)
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"'{config_path}' does not exist. Please check the file path.")

    with open(config_path, 'r') as file:
        return json.load(file)



