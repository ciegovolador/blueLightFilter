# Blue Light Filter GUI

A blue light filter GUI for Lubuntu using xrandr gamma control. Zero external dependencies — uses only Python stdlib.

## Quick Start

```bash
# Run the app
python3 main.py
# or
python3 -m bluelight
```

## Prerequisites

```bash
# tkinter (usually pre-installed)
sudo apt install python3-tk

# xrandr (display control)
sudo apt install x11-xserver-utils
```

## Project Structure

```
bluelight/
├── __init__.py          # Package exports
├── __main__.py          # python -m bluelight entry point
├── color/
│   ├── __init__.py      # gamma_to_hex(), warmth_label()
│   └── tests.py
├── config/
│   ├── __init__.py      # load_config(), save_config()
│   └── tests.py
├── display/
│   ├── __init__.py      # xrandr: detect, apply, build command
│   └── tests.py
├── theme/
│   ├── __init__.py      # Colors, fonts, presets
│   └── tests.py
└── gui/
    ├── __init__.py
    ├── app.py           # Main App window
    ├── slider.py        # Custom canvas slider widget
    └── tests.py
main.py                  # Thin entry point
```

Each feature folder contains its code and colocated tests.

### Modules

| Folder | Purpose |
|--------|---------|
| `color/` | RGB gamma to hex conversion, warmth labels |
| `config/` | Persistent settings in `~/.config/bluelight/settings.json` |
| `display/` | xrandr wrapper — detect displays, apply gamma, build commands |
| `theme/` | Color palette, font definitions, preset configurations |
| `gui/` | Tkinter App class and custom Slider widget |

## Testing

```bash
# Run all tests
python3 -m unittest discover -p "tests.py" -v

# Run tests for a single feature
python3 -m unittest bluelight.color.tests -v
python3 -m unittest bluelight.config.tests -v
python3 -m unittest bluelight.display.tests -v
python3 -m unittest bluelight.theme.tests -v
python3 -m unittest bluelight.gui.tests -v
```

## Building a Binary

Requires [PyInstaller](https://pyinstaller.org/):

```bash
pip install pyinstaller

pyinstaller --onefile --name blue-light-filter main.py
```

The binary will be in `dist/blue-light-filter`.

## License

See [LICENSE](LICENSE).
