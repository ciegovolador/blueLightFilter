"""Configuration file management for Blue Light Filter."""

import json
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "bluelight"
CONFIG_FILE = CONFIG_DIR / "settings.json"


def load_config(path=None):
    """Load saved gamma settings from config file.

    Returns:
        dict: {'r': float, 'g': float, 'b': float} or empty dict if not found.
    """
    cfg = Path(path) if path else CONFIG_FILE
    if cfg.exists():
        try:
            with open(cfg, 'r') as f:
                data = json.load(f)
                return {
                    'r': float(data.get('r', 1.0)),
                    'g': float(data.get('g', 1.0)),
                    'b': float(data.get('b', 1.0))
                }
        except (json.JSONDecodeError, ValueError, TypeError):
            pass
    return {}


def save_config(r, g, b, path=None):
    """Save gamma settings to config file.

    Returns:
        bool: True if saved successfully.
    """
    cfg = Path(path) if path else CONFIG_FILE
    try:
        cfg.parent.mkdir(parents=True, exist_ok=True)
        with open(cfg, 'w') as f:
            json.dump({'r': round(r, 2), 'g': round(g, 2), 'b': round(b, 2)}, f)
        return True
    except Exception:
        return False
