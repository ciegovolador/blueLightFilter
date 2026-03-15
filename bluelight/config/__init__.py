"""Configuration file management for Blue Light Filter."""

import json
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "bluelight"
CONFIG_FILE = CONFIG_DIR / "settings.json"


def _normalize_rgb(data):
    """Extract r, g, b from dict with float conversion and 1.0 defaults."""
    return {
        'r': float(data.get('r', 1.0)),
        'g': float(data.get('g', 1.0)),
        'b': float(data.get('b', 1.0))
    }


def _load_json_file(path):
    """Read and parse a JSON file, returning {} on any error."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError, TypeError, FileNotFoundError, OSError):
        return {}


def load_config(path=None):
    """Load saved gamma settings from config file.

    Supports both legacy format {'r','g','b'} and multi-monitor
    format {'monitors': {'OUTPUT': {'r','g','b'}, ...}}.

    Returns:
        dict: {'r': float, 'g': float, 'b': float} or empty dict if not found.
    """
    cfg = Path(path) if path else CONFIG_FILE
    if not cfg.exists():
        return {}
    data = _load_json_file(cfg)
    if not data:
        return {}
    if 'monitors' in data:
        return data
    return _normalize_rgb(data)


def load_monitor_config(output=None, path=None):
    """Load gamma settings for a specific monitor.

    Args:
        output: Monitor output name (e.g., "HDMI-1"). If None, returns defaults.
        path: Optional config file path override.

    Returns:
        dict: {'r': float, 'g': float, 'b': float} or empty dict.
    """
    data = load_config(path)
    if 'monitors' in data and output:
        mon = data['monitors'].get(output, {})
        return _normalize_rgb(mon) if mon else {}
    if 'r' in data:
        return data
    return {}


def save_config(r, g, b, path=None, output=None):
    """Save gamma settings to config file.

    Args:
        r, g, b: Gamma values.
        path: Optional config file path override.
        output: Monitor output name. If provided, saves per-monitor.

    Returns:
        bool: True if saved successfully.
    """
    cfg = Path(path) if path else CONFIG_FILE
    try:
        cfg.parent.mkdir(parents=True, exist_ok=True)
        values = {'r': round(r, 2), 'g': round(g, 2), 'b': round(b, 2)}

        if output:
            existing = _load_json_file(cfg) if cfg.exists() else {}

            if 'monitors' not in existing:
                # Migrate legacy format
                existing = {'monitors': {}}
            existing['monitors'][output] = values

            with open(cfg, 'w') as f:
                json.dump(existing, f)
        else:
            with open(cfg, 'w') as f:
                json.dump(values, f)
        return True
    except Exception:
        return False
