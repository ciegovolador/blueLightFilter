## MODIFIED Requirements

### Requirement: Persistent Configuration
The config module SHALL normalize legacy single-monitor format `{"r": x, "g": y, "b": z}` into multi-monitor format `{"monitors": {"primary": {"r": x, "g": y, "b": z}}}` at load time, using shared `_normalize_rgb()` and `_load_json_file()` helpers internally. External behavior (load/save results) SHALL remain identical.

#### Scenario: Legacy config loaded
- **WHEN** a config file contains `{"r": 1.0, "g": 0.85, "b": 0.65}`
- **THEN** `load_monitor_config("HDMI-1")` returns `{"r": 1.0, "g": 0.85, "b": 0.65}`

#### Scenario: Multi-monitor config loaded
- **WHEN** a config file contains `{"monitors": {"HDMI-1": {"r": 0.8, "g": 0.7, "b": 0.5}}}`
- **THEN** `load_monitor_config("HDMI-1")` returns `{"r": 0.8, "g": 0.7, "b": 0.5}`

#### Scenario: Missing config file
- **WHEN** no config file exists
- **THEN** `load_monitor_config("HDMI-1")` returns `{"r": 1.0, "g": 1.0, "b": 1.0}`
