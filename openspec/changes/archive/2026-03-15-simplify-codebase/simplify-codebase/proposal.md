## Why

The codebase has accumulated duplication and complexity as features were added incrementally. The `App` class handles too many concerns (~360 lines, 8+ responsibilities), config loading logic is duplicated, and several utility functions exist that are unused or trivially inlineable. Simplifying now reduces maintenance burden and makes the code easier to extend.

## What Changes

- Extract duplicated RGB normalization and JSON loading in `config/` into shared helpers
- Consolidate duplicated slider/label update logic and button styling in `gui/app.py` into helper methods
- Inline or remove unused utility functions (`get_connected_output()`, `gamma_string()`)
- Replace "All Monitors" magic string with a cleaner sentinel pattern
- Extract grouped widget update logic to reduce repetition in callbacks
- Simplify config loading by normalizing legacy format on load

## Non-goals

- Changing the folder structure or module architecture
- Adding new features or changing existing behavior
- Modifying the UI appearance or theme
- Extracting the App class into multiple classes (too invasive for this change)

## Capabilities

### New Capabilities

- `dry-config-helpers`: Extract shared config helpers (_normalize_rgb, _load_json_file) to eliminate duplication in load/save paths
- `dry-gui-helpers`: Consolidate duplicated GUI update patterns (slider+label sync, button styling, target iteration) into reusable methods
- `yagni-cleanup`: Remove or inline unused/trivial utility functions (get_connected_output, gamma_string, _card)

### Modified Capabilities

- `blue-light-filter`: Config loading normalizes legacy format earlier; internal helper methods change but external behavior is identical

## Impact

- **Code**: `bluelight/config/__init__.py`, `bluelight/display/__init__.py`, `bluelight/gui/app.py`
- **Tests**: Test files for config and display modules may need updates for removed/renamed functions
- **APIs**: `get_connected_output()` and `gamma_string()` removed from public API (unused externally)
- **Behavior**: No user-facing changes
