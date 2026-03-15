## Context

The Blue Light Filter app is a Python/tkinter desktop tool with a modular architecture: `color/`, `config/`, `display/`, `theme/`, `gui/`. Over time, code duplication crept in — especially in `config/__init__.py` (duplicate RGB normalization and JSON loading) and `gui/app.py` (duplicate slider/label updates, button styling, target iteration). Several utility functions are unused or trivially inlineable.

## Goals / Non-Goals

**Goals:**
- Eliminate code duplication in config and GUI modules
- Remove unused utility functions
- Simplify config loading by normalizing legacy format early
- Keep all existing tests passing with minimal test changes

**Non-Goals:**
- Restructuring folders or module boundaries
- Extracting App into multiple classes
- Changing UI appearance or behavior
- Adding dependency injection or abstract interfaces

## Decisions

### 1. Extract `_normalize_rgb()` and `_load_json_file()` in config module

**Choice**: Private helper functions in `config/__init__.py`.
**Rationale**: These are internal implementation details, not public API. Private functions keep the module's public surface unchanged. Considered a shared utils module but YAGNI — only config needs these.

### 2. Consolidate GUI update patterns into `_set_rgb()` helper

**Choice**: Single `_set_rgb(r, g, b, preset_idx=-1)` method that updates sliders, labels, and internal state.
**Rationale**: Both `_preset()` and `_monitor_changed()` perform identical slider/label updates. A shared method eliminates 15+ duplicate lines. Considered a separate class but that's too invasive for this scope.

### 3. Inline `gamma_string()` into `build_command()`

**Choice**: Remove `gamma_string()`, inline the f-string into `build_command()`.
**Rationale**: One-liner used in exactly one place. The function adds API surface without value. Tests for `gamma_string()` will be removed; the formatting is still tested via `build_command()` tests.

### 4. Remove `get_connected_output()`

**Choice**: Delete the function entirely.
**Rationale**: Not called anywhere in the application code. It was a pre-multi-monitor convenience that's now obsolete. Only referenced in its own tests.

### 5. Consolidate button styling

**Choice**: Extract common button kwargs into a dict constant or `_make_button()` helper in app.py.
**Rationale**: Preset buttons and action buttons share ~8 identical kwargs. A shared base reduces duplication while keeping customization per button type.

### 6. Extract `_iter_target_gamma()` generator

**Choice**: Single method that yields `(output, r, g, b)` tuples for current targets.
**Rationale**: Three methods (`_apply`, `_copy`, `_save_permanent`) each independently fetch targets, check emptiness, and iterate. A generator centralizes this pattern.

## Risks / Trade-offs

- **[Risk] Removing public functions breaks external consumers** → Mitigated: `get_connected_output()` and `gamma_string()` are not used outside tests. This is a standalone desktop app with no external consumers.
- **[Risk] Test changes could mask regressions** → Mitigated: Remove tests only for deleted functions. All behavioral tests remain. Run full suite after each change.
- **[Trade-off] Helper methods add indirection** → Acceptable: The helpers replace duplication, and each is ≤5 lines. Net code is shorter and clearer.
