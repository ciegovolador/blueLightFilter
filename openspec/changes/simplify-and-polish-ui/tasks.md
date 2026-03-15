## 1. Theme Updates

- [x] 1.1 Add proportional font constants (`FONT`, `FONT_B`, `FONT_S`, `FONT_LG`) to `bluelight/theme/__init__.py` using `TkDefaultFont`
- [x] 1.2 Update theme tests to validate new font constants

## 2. Simplified Slider

- [x] 2.1 Rewrite `bluelight/gui/slider.py`: change from `tk.Canvas` to `tk.Frame` containing Canvas (fill) + Scale (interaction)
- [x] 2.2 Update slider tests in `bluelight/gui/tests.py` for new widget structure

## 3. Consolidated Config

- [x] 3.1 Replace `load_config`/`load_monitor_config` with `load_settings(output=None)` in `bluelight/config/__init__.py`; always return defaults dict
- [x] 3.2 Add backward-compat aliases (`load_config`, `load_monitor_config`, `save_config`)
- [x] 3.3 Rename `save_config` to `save_settings` with alias
- [x] 3.4 Update config tests for new return values (defaults instead of empty dict)

## 4. UI Polish - App Class

- [x] 4.1 Update imports in `app.py` to use new font constants and `load_settings`
- [x] 4.2 Increase padding: window edge padx to 24, card inner padding to 18, separator gaps to 10
- [x] 4.3 Enlarge preview swatch from 54x54 to 64x64
- [x] 4.4 Update `_build_header` to use proportional fonts for title and subtitle
- [x] 4.5 Update section labels ("PRESETS", "MANUAL CONTROL", "GENERATED COMMAND") to use proportional font
- [x] 4.6 Add hover effects to `_btn` helper: bind `<Enter>`/`<Leave>` for bg color toggle
- [x] 4.7 Add hover effects to preset buttons

## 5. Verification

- [x] 5.1 Run full test suite and fix any failures
- [x] 5.2 Launch app manually and verify UI renders correctly
