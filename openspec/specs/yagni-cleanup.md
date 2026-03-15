# YAGNI Cleanup — Spec

## Requirements

### Requirement: Remove unused get_connected_output function
The display module SHALL NOT export `get_connected_output()`. The function SHALL be deleted along with its tests.

#### Scenario: Function is removed
- **WHEN** a caller imports from `bluelight.display`
- **THEN** `get_connected_output` is not available
- **THEN** `get_connected_outputs` (plural) remains available

### Requirement: Inline gamma_string into build_command
The display module SHALL NOT export `gamma_string()`. The formatting logic SHALL be inlined into `build_command()`.

#### Scenario: build_command still formats correctly
- **WHEN** `build_command("HDMI-1", 1.0, 0.85, 0.65)` is called
- **THEN** it returns `"xrandr --output HDMI-1 --gamma 1.00:0.85:0.65"`

#### Scenario: gamma_string is removed
- **WHEN** a caller imports from `bluelight.display`
- **THEN** `gamma_string` is not available
