# Blue Light Filter — Application Spec

## Overview

A tkinter-based desktop GUI for adjusting display gamma via xrandr to reduce blue light emission on Lubuntu/Openbox. Supports multi-monitor setups with per-display settings and persistent configuration.

## Target Environment

- **OS**: Lubuntu / Openbox desktop
- **Runtime**: Python 3 (stdlib only — no external dependencies)
- **Display server**: X11 (xrandr required)
- **Config location**: `~/.config/bluelight/settings.json`

## Architecture

```
bluelight/
├── __init__.py          # Package exports (App)
├── __main__.py          # `python -m bluelight` entry point
├── color/               # Gamma-to-hex conversion, warmth labels
├── config/              # JSON config read/write (~/.config/bluelight/)
├── display/             # xrandr detection, command building, execution
├── theme/               # Dark color palette, fonts, preset definitions
└── gui/
    ├── app.py           # Main App(tk.Tk) window
    └── slider.py        # Custom Canvas-based slider widget
```

Entry points: `python3 main.py` or `python3 -m bluelight`.

## Features

### 1. Multi-Monitor Support

- Detect connected displays via `xrandr` output parsing.
- Per-monitor gamma values stored in `_monitor_gamma` dict.
- Monitor selector dropdown (visible when ≥ 2 displays detected).
- "All Monitors" option applies identical gamma to every display.
- Status indicator: green = displays found, red = none detected.

### 2. RGB Gamma Control

- Three independent sliders for Red, Green, Blue channels.
- Range: 0.10 – 1.00 (step resolution via mouse drag).
- Changes update preview and command display in real time.

### 3. Presets

| Name       | R    | G    | B    | Description       |
|------------|------|------|------|-------------------|
| Daylight   | 1.00 | 1.00 | 1.00 | No filtering      |
| Reading    | 1.00 | 0.95 | 0.85 | Slight warmth     |
| Evening    | 1.00 | 0.85 | 0.65 | Moderate warmth   |
| Night      | 1.00 | 0.75 | 0.50 | Warm orange       |
| Deep Night | 1.00 | 0.60 | 0.35 | Maximum warmth    |

Preset buttons highlight when active (exact match on R/G/B).

### 4. Visual Feedback

- **Color swatch**: live preview orb showing current gamma as hex color.
- **Warmth label**: text descriptor based on blue channel value:
  - ≥ 0.95 → "Cool - daylight"
  - ≥ 0.82 → "Slightly warm"
  - ≥ 0.65 → "Warm"
  - ≥ 0.50 → "Hot"
  - < 0.50 → "Max warm"
- **RGB values**: numeric R, G, B shown in preview card.
- **Command display**: shows the exact `xrandr --output <NAME> --gamma R:G:B` command(s).

### 5. Actions

| Button          | Behavior                                                       |
|-----------------|----------------------------------------------------------------|
| Apply Now       | Execute xrandr gamma command on target display(s)              |
| Save Permanently| Write per-monitor settings to `settings.json`                  |
| Reset           | Set all channels to 1.0 (daylight) on target display(s)       |
| Copy CMD        | Copy generated xrandr command(s) to system clipboard           |

### 6. Status Messages

Temporary flash messages (2.8s) at bottom of window:
- **Green**: success (applied, saved, copied, reset).
- **Red**: error (xrandr not found, save failed, no displays).

### 7. Persistent Configuration

The config module normalizes legacy single-monitor format into multi-monitor format at load time, using shared `_normalize_rgb()` and `_load_json_file()` helpers internally. External behavior (load/save results) remains identical.

**Multi-monitor format** (current):
```json
{
  "monitors": {
    "HDMI-1": {"r": 1.0, "g": 0.85, "b": 0.65},
    "eDP-1": {"r": 1.0, "g": 0.75, "b": 0.50}
  }
}
```

**Legacy format** (auto-migrated on load):
```json
{"r": 1.0, "g": 0.85, "b": 0.65}
```

On startup: load config → apply saved gamma to all displays → render UI.

## UI Design

- **Theme**: dark (background `#0d0d15`, card `#13131e`, accent `#ff9944`).
- **Font**: Courier New (9pt, 10pt, 19pt bold).
- **Window**: fixed size, non-resizable.
- **Layout**: card-based sections with horizontal button rows.

## xrandr Integration

- Detection: `xrandr` stdout parsed for lines containing ` connected`.
- Availability check: `shutil.which("xrandr")` at startup.
- Execution: `subprocess.Popen` with stdout/stderr suppressed.
- Command format: `xrandr --output <OUTPUT> --gamma R.RR:G.GG:B.BB`

## Color Conversion

`gamma_to_hex(r, g, b)` maps gamma floats to hex with weighted scaling:
- Red: `int(r * 255)`
- Green: `int(185*g + 40)`, clamped 0–255
- Blue: `int(140*b + 20)`, clamped 0–255

This biases the preview toward warm tones matching perceived screen color.

## Error Handling

| Condition              | Behavior                                           |
|------------------------|----------------------------------------------------|
| xrandr missing         | Red flash: "xrandr not found — install x11-xserver-utils" |
| No displays detected   | Red status label, apply/reset operations disabled  |
| Config file missing    | Auto-create with defaults                          |
| Invalid/empty config   | Fall back to Evening preset (1.0, 0.85, 0.65)     |
| Save failure           | Red flash with error details                       |

## Testing

```bash
python3 -m unittest discover -p "tests.py" -v
```

Tests are colocated in each module directory as `tests.py`.
