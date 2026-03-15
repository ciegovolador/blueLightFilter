## Why

The app works well but the GUI code is dense and the UI looks utilitarian. The `App` class at 369 lines mixes widget construction, styling, state management, and callbacks. The Courier New monospace font everywhere gives a "terminal" feel rather than a polished desktop app. Spacing, padding, and visual hierarchy could be improved to make the UI more inviting without adding dependencies.

## What Changes

- Refactor `App` class: extract widget construction into a declarative builder pattern, reducing the class to orchestration + callbacks
- Polish the UI: increase padding, add rounded card corners via Canvas, improve font hierarchy with proportional fonts (system default) for labels and monospace only for values/commands
- Simplify the slider module: replace the custom Canvas slider with a hybrid Canvas-fill + tkinter Scale approach for native behavior with colored fill
- Consolidate config API: merge `load_config`/`load_monitor_config` into single `load_settings(output=None)` that always returns defaults
- Improve visual polish: better color preview (larger swatch), cleaner preset buttons with hover states, more breathing room between sections

## Non-goals

- Adding external dependencies (stays stdlib-only)
- Changing xrandr integration or display detection logic
- Adding new features (scheduling, auto-detect, etc.)
- Restructuring the module/folder layout

## Capabilities

### New Capabilities

- `polished-ui`: Improved spacing, font hierarchy, card styling, hover effects, and visual breathing room across all UI sections
- `simplified-slider`: Hybrid Canvas-fill + Scale slider replacing the fully custom Canvas implementation
- `consolidated-config`: Single `load_settings(output=None)` function replacing dual load functions, always returning usable defaults

### Modified Capabilities

- `blue-light-filter`: UI appearance changes (fonts, spacing, card styling) while maintaining identical behavior
- `dry-gui-helpers`: `_btn` helper updated to support hover states; `_card` method updated for improved styling

## Impact

- **Code**: `bluelight/gui/app.py` (major refactor), `bluelight/gui/slider.py` (rewrite), `bluelight/config/__init__.py` (API simplification), `bluelight/theme/__init__.py` (font updates)
- **Tests**: Slider tests updated for new widget type; config tests updated for new return values (defaults instead of empty dict)
- **APIs**: Config public API changes (`load_settings` replaces two functions); backward-compat aliases provided
- **Behavior**: UI looks different (prettier) but all functionality is identical
