## Context

The Blue Light Filter app is a Python/tkinter desktop tool (~680 lines of source) with a dark-themed UI. After a previous simplification pass (DRY helpers, YAGNI cleanup), the code is cleaner but still has opportunities: the `App` class is 369 lines mixing construction and logic, the custom Canvas slider reimplements native behavior, the config module exposes two overlapping load functions, and the UI uses Courier New everywhere which looks more "terminal" than "app". All changes must remain zero-dependency (stdlib + tkinter only).

## Goals / Non-Goals

**Goals:**
- Reduce `App` class complexity by extracting UI construction into smaller, focused methods
- Replace the custom Canvas slider with a Canvas-fill + Scale hybrid for native behavior + colored fill
- Unify config loading into a single function returning usable defaults
- Polish UI: better font hierarchy, more padding, hover states on buttons, larger preview swatch
- Keep all 70 existing tests passing (update as needed for API changes)

**Non-Goals:**
- Adding external dependencies or pip packages
- Restructuring folder layout or module boundaries
- Adding new features (scheduling, profiles, system tray)
- Switching away from tkinter

## Decisions

### 1. Hybrid Slider: Canvas fill + tkinter Scale

**Choice**: `Slider(tk.Frame)` containing a Canvas (colored fill bar) stacked above a tkinter Scale (interaction).

**Rationale**: The current custom `Slider(tk.Canvas)` at 82 lines reimplements click, drag, coordinate conversion, and drawing. tkinter's Scale handles all interaction natively. We only need Canvas for the colored fill visualization. Combining them gives native behavior (keyboard support, accessibility) with the visual style.

**Alternatives considered**:
- Keep custom Canvas slider: works, but maintains 80+ lines of custom interaction code
- Use Scale alone: loses colored fill visualization
- Style Scale with ttk: ttk theming on Linux/tk 8.6 is fragile and still can't do colored fill

### 2. Font hierarchy: system proportional + monospace for values

**Choice**: Use `TkDefaultFont` for labels/headings, keep monospace only for numeric values and the command box.

**Rationale**: Courier New everywhere gives a "hacker terminal" look. Mixing proportional fonts for UI labels (section headers, button text, warmth label) with monospace for data (RGB values, xrandr command) creates a clearer visual hierarchy. `TkDefaultFont` is guaranteed available on all tkinter installations.

**Alternatives considered**:
- Use a specific font like "Segoe UI" or "Noto Sans": not reliably available across Linux distros
- Keep all Courier New: works but looks utilitarian

### 3. Single `load_settings()` config function

**Choice**: Replace `load_config()` + `load_monitor_config()` with `load_settings(output=None)` that always returns `{'r': float, 'g': float, 'b': float}` (defaults to 1.0).

**Rationale**: Two functions with overlapping logic and different return contracts (one returns raw dict with `monitors` key, other returns flat RGB) creates confusion. The app always needs flat RGB values per-monitor. Returning defaults instead of empty dict eliminates null-checking at every call site. Backward-compat aliases kept for test compatibility.

### 4. Button hover effects via bind/unbind

**Choice**: Add `<Enter>`/`<Leave>` bindings on buttons to change background color on hover.

**Rationale**: tkinter buttons have `activebackground` for click state but no hover state by default. Binding mouse enter/leave events to change `bg` is the simplest stdlib approach. No ttk or custom widget needed.

### 5. Increased spacing and card padding

**Choice**: Increase all `padx` from 22 to 24, increase card inner padding from 14-16 to 18, increase section vertical gaps.

**Rationale**: The current UI feels cramped. Small padding increases create breathing room without increasing window size significantly. Matches modern desktop app conventions.

## Risks / Trade-offs

- **[Risk] Font rendering differences across distros** -> Mitigated: `TkDefaultFont` is a tkinter virtual font that always resolves to something usable. Fallback is guaranteed.
- **[Risk] Scale widget looks different across tk versions** -> Acceptable: Scale is a core tkinter widget, visually consistent enough. The Canvas fill overlay maintains our brand color.
- **[Risk] Backward-compat aliases in config add maintenance** -> Low risk: aliases are one-liners. Can remove in a future breaking change.
- **[Trade-off] UI appearance changes may surprise existing users** -> Acceptable: the app is a personal tool for Lubuntu, not a widely-distributed product. Better aesthetics outweigh visual stability.
