## ADDED Requirements

### Requirement: Single load function with defaults

The config module SHALL expose a single `load_settings(output=None, path=None)` function that always returns a dict with `r`, `g`, `b` float keys.

#### Scenario: No config file exists
- **WHEN** `load_settings()` is called and no config file exists
- **THEN** it SHALL return `{'r': 1.0, 'g': 1.0, 'b': 1.0}`

#### Scenario: Load specific monitor settings
- **WHEN** `load_settings(output="HDMI-1")` is called with a valid multi-monitor config
- **THEN** it SHALL return `{'r': float, 'g': float, 'b': float}` for that monitor

#### Scenario: Monitor not in config
- **WHEN** `load_settings(output="UNKNOWN")` is called and the monitor is not in the config
- **THEN** it SHALL return `{'r': 1.0, 'g': 1.0, 'b': 1.0}`

#### Scenario: Legacy format compatibility
- **WHEN** `load_settings(output="HDMI-1")` is called on a legacy `{'r','g','b'}` config file
- **THEN** it SHALL return those values for any output name

### Requirement: Backward compatibility aliases

The config module SHALL provide `load_config`, `load_monitor_config`, and `save_config` as aliases to maintain backward compatibility.

#### Scenario: Alias functions work
- **WHEN** `load_monitor_config("HDMI-1")` is called
- **THEN** it SHALL behave identically to `load_settings(output="HDMI-1")`
