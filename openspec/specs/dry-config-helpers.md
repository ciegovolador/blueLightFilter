# DRY Config Helpers — Spec

## Requirements

### Requirement: Shared RGB normalization helper
The config module SHALL provide a private `_normalize_rgb(data)` function that extracts r, g, b values from a dict, converting to float with a default of 1.0 for missing keys.

#### Scenario: Complete RGB data
- **WHEN** `_normalize_rgb({"r": 0.8, "g": 0.7, "b": 0.5})` is called
- **THEN** it returns `{"r": 0.8, "g": 0.7, "b": 0.5}`

#### Scenario: Missing keys use defaults
- **WHEN** `_normalize_rgb({"r": 0.8})` is called
- **THEN** it returns `{"r": 0.8, "g": 1.0, "b": 1.0}`

#### Scenario: Empty dict
- **WHEN** `_normalize_rgb({})` is called
- **THEN** it returns `{"r": 1.0, "g": 1.0, "b": 1.0}`

### Requirement: Shared JSON file loader
The config module SHALL provide a private `_load_json_file(path)` function that reads and parses a JSON file, returning an empty dict on any error (missing file, invalid JSON).

#### Scenario: Valid JSON file
- **WHEN** `_load_json_file(path)` is called with a path to a valid JSON file containing `{"r": 0.5}`
- **THEN** it returns `{"r": 0.5}`

#### Scenario: Missing file
- **WHEN** `_load_json_file(path)` is called with a nonexistent path
- **THEN** it returns `{}`

#### Scenario: Invalid JSON
- **WHEN** `_load_json_file(path)` is called with a file containing invalid JSON
- **THEN** it returns `{}`
