# DRY GUI Helpers — Spec

## Requirements

### Requirement: Unified RGB update method
The App class SHALL provide a `_set_rgb(r, g, b, preset_idx=-1)` method that updates internal state, slider positions, value labels, and preset highlighting in a single call.

#### Scenario: Preset applies RGB values
- **WHEN** `_set_rgb(1.0, 0.85, 0.65, preset_idx=2)` is called
- **THEN** `self._r, self._g, self._b` are set to `1.0, 0.85, 0.65`
- **THEN** sliders `_sl_r, _sl_g, _sl_b` are positioned to those values
- **THEN** labels `_rl, _gl, _bl` display `"1.00"`, `"0.85"`, `"0.65"`
- **THEN** preset button at index 2 is highlighted

#### Scenario: Monitor change applies RGB values
- **WHEN** `_set_rgb(1.0, 0.75, 0.50)` is called without preset_idx
- **THEN** state, sliders, and labels are updated
- **THEN** no preset button is highlighted (default index -1)

### Requirement: Consolidated button styling
The App class SHALL use a shared base style dict or helper for button creation, reducing duplicated kwargs across preset buttons and action buttons.

#### Scenario: Preset button uses shared style
- **WHEN** a preset button is created
- **THEN** it uses the shared base style (bg, fg, relief, bd, highlightthickness, cursor)

#### Scenario: Action button uses shared style with overrides
- **WHEN** an action button is created with `primary=True`
- **THEN** it uses the shared base style with accent color overrides

### Requirement: Target gamma iterator
The App class SHALL provide a `_iter_target_gamma()` method that yields `(output, r, g, b)` tuples for all current target outputs.

#### Scenario: Single monitor selected
- **WHEN** a specific monitor is selected in the dropdown
- **THEN** `_iter_target_gamma()` yields one tuple with that monitor's gamma values

#### Scenario: All monitors selected
- **WHEN** "All Monitors" is selected
- **THEN** `_iter_target_gamma()` yields tuples for every connected display
