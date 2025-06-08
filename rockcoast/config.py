# This module handles loading configuration parameters from a JSON file.

import json
import os
class ConfigError(Exception):
    """Custom exception for configuration loading errors."""
    pass

def load_config(config_path):
    """
    Load simulation configuration from a JSON file.

    Parameters:
    - config_path (str): path to the JSON configuration file

    Returns:
    - config (dict): configuration parameters
    """
    if not os.path.exists(config_path):
        raise ConfigError(f"Config file not found: {config_path}")

    with open(config_path, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            raise ConfigError("Invalid JSON format.")

    return config
