# Blue Light Filter GUI

A cross-platform blue light filter GUI for Lubuntu using xrandr gamma control. Zero external dependencies — uses only Python stdlib.

## File Structure

The application has been refactored into modular components for better readability and maintainability:

### `main.py`
Entry point for the application. Simply runs the GUI.

### `ui.py`
**Main GUI Application** — `App` class
- Constructs the entire user interface
- Manages all button callbacks and event handlers
- Updates UI state based on user interactions
- ~210 lines, focused solely on UI logic

### `slider.py`
**Custom Slider Widget** — `Slider` class
- Canvas-based horizontal slider (no external dependencies)
- Handles mouse clicks and drag events
- Independent, reusable widget component
- ~80 lines

### `constants.py`
**Theme & Configuration**
- Color palette (background, accent, text, etc.)
- Font definitions
- Preset configurations (Daylight, Reading, Evening, Night, Deep Night)
- ~30 lines

### `xrandr_utils.py`
**Display Control Utilities**
- `get_connected_output()` — Detects connected display
- `apply_gamma()` — Applies gamma adjustment to display
- `build_command()` — Generates xrandr command string
- `has_xrandr()` — Checks if xrandr is installed
- ~55 lines

### `color_utils.py`
**Color Conversion**
- `gamma_to_hex()` — Converts RGB gamma values to hex color for preview
- `warmth_label()` — Returns human-readable warmth label
- ~35 lines

## Usage

```bash
python3 main.py
```

## Installation

If tkinter is missing:
```bash
sudo apt install python3-tk
```

For xrandr support:
```bash
sudo apt install x11-xserver-utils
```

## Benefits of This Structure

✓ **Separation of Concerns** — Each module has a single responsibility
✓ **Readability** — Easier to understand and navigate the codebase
✓ **Reusability** — Components can be used in other projects
✓ **Testability** — Utilities can be unit tested independently
✓ **Maintainability** — Changes are isolated to relevant modules
✓ **Scalability** — Easy to add new features without cluttering files
