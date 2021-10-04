from pathlib import Path
import json


def get_layout_config(filepath: Path):
    with open(filepath, encoding='utf-8') as f:
        return json.load(f)
