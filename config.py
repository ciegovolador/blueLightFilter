"""Configuration file management for Blue Light Filter."""

import json
import os
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "bluelight"
CONFIG_FILE = CONFIG_DIR / "settings.json"


def load_config():
    """Load saved gamma settings from config file.

    Returns:
        dict: {'r': float, 'g': float, 'b': float} or empty dict if not found.
    """
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                return {
                    'r': float(data.get('r', 1.0)),
                    'g': float(data.get('g', 1.0)),
                    'b': float(data.get('b', 1.0))
                }
        except (json.JSONDecodeError, ValueError, TypeError):
            pass
    return {}


def save_config(r, g, b):
    """Save gamma settings to config file.

    Args:
        r (float): Red gamma value.
        g (float): Green gamma value.
        b (float): Blue gamma value.

    Returns:
        bool: True if saved successfully.
    """
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump({'r': round(r, 2), 'g': round(g, 2), 'b': round(b, 2)}, f)
        return True
    except Exception:
        return False
