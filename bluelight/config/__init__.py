"""Configuration file management for Blue Light Filter."""

import json
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "bluelight"
CONFIG_FILE = CONFIG_DIR / "settings.json"

DEFAULTS = {"r": 1.0, "g": 1.0, "b": 1.0}


def _load_json(path):
    """Read and parse JSON file, return {} on error."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError, TypeError, FileNotFoundError, OSError):
        return {}


def _normalize(data):
    """Extract r, g, b from dict with defaults."""
    return {
        "r": float(data.get("r", 1.0)),
        "g": float(data.get("g", 1.0)),
        "b": float(data.get("b", 1.0)),
    }


def load_settings(output=None, path=None):
    """Load gamma settings from config file.

    Args:
        output: Monitor output name. If provided, load for that monitor.
        path: Optional config file path override.

    Returns:
        dict: {'r': float, 'g': float, 'b': float} — defaults if not found.
    """
    cfg = Path(path) if path else CONFIG_FILE
    if not cfg.exists():
        return DEFAULTS.copy()

    data = _load_json(cfg)
    if not data:
        return DEFAULTS.copy()

    # Legacy format: flat {'r', 'g', 'b'}
    if "monitors" not in data and "r" in data:
        return _normalize(data)

    # Multi-monitor format
    if output and "monitors" in data:
        mon = data["monitors"].get(output)
        if mon:
            return _normalize(mon)

    return DEFAULTS.copy()


def save_settings(r, g, b, path=None, output=None):
    """Save gamma settings to config file.

    Args:
        r, g, b: Gamma values (0.0–1.0).
        path: Optional config file path override.
        output: Monitor output name. If provided, saves per-monitor.

    Returns:
        bool: True if saved successfully.
    """
    cfg = Path(path) if path else CONFIG_FILE
    try:
        cfg.parent.mkdir(parents=True, exist_ok=True)
        values = {"r": round(r, 2), "g": round(g, 2), "b": round(b, 2)}

        if output:
            existing = _load_json(cfg) if cfg.exists() else {}
            if "monitors" not in existing:
                existing = {"monitors": {}}
            existing["monitors"][output] = values
            with open(cfg, "w") as f:
                json.dump(existing, f)
        else:
            with open(cfg, "w") as f:
                json.dump(values, f)
        return True
    except Exception:
        return False


# Backward-compat aliases
load_monitor_config = load_settings
save_config = save_settings


def load_config(path=None):
    """Legacy: load raw config data (for tests that check 'monitors' key)."""
    cfg = Path(path) if path else CONFIG_FILE
    if not cfg.exists():
        return {}
    data = _load_json(cfg)
    if not data:
        return {}
    if "monitors" in data:
        return data
    return _normalize(data)
