## 1. Config DRY Helpers

- [x] 1.1 Add `_normalize_rgb(data)` helper to `bluelight/config/__init__.py` that extracts r/g/b with float conversion and 1.0 defaults
- [x] 1.2 Add `_load_json_file(path)` helper that reads/parses JSON, returns `{}` on any error
- [x] 1.3 Refactor `load_config()` to use `_load_json_file()` and `_normalize_rgb()`
- [x] 1.4 Refactor `load_monitor_config()` to use `_load_json_file()` and `_normalize_rgb()`
- [x] 1.5 Update config tests for new helpers and verify existing tests pass

## 2. YAGNI Cleanup — Display Module

- [x] 2.1 Remove `get_connected_output()` from `bluelight/display/__init__.py`
- [x] 2.2 Inline `gamma_string()` format into `build_command()` and remove the function
- [x] 2.3 Update `bluelight/display/__init__.py` `__all__` or exports if defined
- [x] 2.4 Remove tests for `get_connected_output()` and `gamma_string()` from display tests
- [x] 2.5 Run display tests to verify `build_command()` still works correctly

## 3. GUI DRY Helpers — RGB Update

- [x] 3.1 Add `_set_rgb(r, g, b, preset_idx=-1)` method to App that updates `_r/_g/_b`, sliders, labels, and calls `_highlight_preset()`
- [x] 3.2 Refactor `_preset()` to use `_set_rgb()` instead of inline updates
- [x] 3.3 Refactor `_monitor_changed()` to use `_set_rgb()` instead of inline updates

## 4. GUI DRY Helpers — Button Styling

- [x] 4.1 Extract shared button style dict (bg, fg, relief, bd, cursor, highlight) as a constant or helper in app.py
- [x] 4.2 Refactor preset button creation to use shared style
- [x] 4.3 Refactor `_btn()` action button method to use shared style

## 5. GUI DRY Helpers — Target Iteration

- [x] 5.1 Add `_iter_target_gamma()` generator method that yields `(output, r, g, b)` for current targets
- [x] 5.2 Refactor `_apply()` to use `_iter_target_gamma()`
- [x] 5.3 Refactor `_copy()` to use `_iter_target_gamma()`
- [x] 5.4 Refactor `_save_permanent()` to use `_iter_target_gamma()`

## 6. Verification

- [x] 6.1 Run full test suite (`python3 -m unittest discover -p "tests.py" -v`)
- [x] 6.2 Launch app manually to verify UI behaves identically
