import json
import os
from utils.logger import logger

def load_json_config(filepath):
    if not os.path.exists(filepath):
        error_msg = f"Config file missing: {filepath}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
        raise

def load_all_configs(config_dir="config"):
    configs = {}
    expected_files = [
        "app_config.json",
        "abbreviations.json",
        "brands.json",
        "synonyms.json",
        "sources.json"
    ]

    for filename in expected_files:
        path = os.path.join(config_dir, filename)
        configs[filename.replace(".json", "")] = load_json_config(path)

    return configs
