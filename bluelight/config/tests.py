"""Tests for bluelight.config."""

import json
import tempfile
import unittest
from pathlib import Path
from bluelight.config import (
    load_config,
    load_settings,
    load_monitor_config,
    save_config,
    save_settings,
    DEFAULTS,
)


class TestSaveConfig(unittest.TestCase):
    def test_save_creates_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            result = save_settings(1.0, 0.85, 0.65, path=path)
            self.assertTrue(result)
            self.assertTrue(path.exists())

    def test_save_writes_correct_values(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_settings(1.0, 0.85, 0.65, path=path)
            with open(path) as f:
                data = json.load(f)
            self.assertEqual(data, {"r": 1.0, "g": 0.85, "b": 0.65})

    def test_save_rounds_values(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_settings(0.999, 0.854, 0.651, path=path)
            with open(path) as f:
                data = json.load(f)
            self.assertEqual(data, {"r": 1.0, "g": 0.85, "b": 0.65})

    def test_save_creates_parent_dirs(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "sub" / "dir" / "settings.json"
            result = save_settings(1.0, 1.0, 1.0, path=path)
            self.assertTrue(result)
            self.assertTrue(path.exists())

    def test_save_config_alias(self):
        self.assertIs(save_config, save_settings)


class TestLoadSettings(unittest.TestCase):
    def test_missing_file_returns_defaults(self):
        result = load_settings(path="/nonexistent/path/settings.json")
        self.assertEqual(result, DEFAULTS)

    def test_load_valid_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            with open(path, "w") as f:
                json.dump({"r": 1.0, "g": 0.85, "b": 0.65}, f)
            result = load_settings(path=path)
            self.assertEqual(result, {"r": 1.0, "g": 0.85, "b": 0.65})

    def test_corrupt_json_returns_defaults(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            with open(path, "w") as f:
                f.write("{broken json")
            result = load_settings(path=path)
            self.assertEqual(result, DEFAULTS)

    def test_missing_keys_default_to_1(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            with open(path, "w") as f:
                json.dump({"r": 0.5}, f)
            result = load_settings(path=path)
            self.assertEqual(result, {"r": 0.5, "g": 1.0, "b": 1.0})

    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_settings(1.0, 0.75, 0.50, path=path)
            result = load_settings(path=path)
            self.assertEqual(result, {"r": 1.0, "g": 0.75, "b": 0.5})

    def test_load_monitor_config_alias(self):
        self.assertIs(load_monitor_config, load_settings)


class TestMultiMonitorConfig(unittest.TestCase):
    def test_save_per_monitor(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_settings(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            with open(path) as f:
                data = json.load(f)
            self.assertIn("monitors", data)
            self.assertEqual(
                data["monitors"]["HDMI-1"], {"r": 1.0, "g": 0.85, "b": 0.65}
            )

    def test_save_multiple_monitors(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_settings(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            save_settings(1.0, 0.75, 0.50, path=path, output="eDP-1")
            with open(path) as f:
                data = json.load(f)
            self.assertEqual(
                data["monitors"]["HDMI-1"], {"r": 1.0, "g": 0.85, "b": 0.65}
            )
            self.assertEqual(data["monitors"]["eDP-1"], {"r": 1.0, "g": 0.75, "b": 0.5})

    def test_save_overwrites_existing_monitor(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_settings(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            save_settings(1.0, 0.60, 0.35, path=path, output="HDMI-1")
            result = load_settings("HDMI-1", path=path)
            self.assertEqual(result, {"r": 1.0, "g": 0.6, "b": 0.35})

    def test_save_preserves_other_monitors(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_settings(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            save_settings(1.0, 0.75, 0.50, path=path, output="eDP-1")
            save_settings(1.0, 0.60, 0.35, path=path, output="HDMI-1")
            self.assertEqual(
                load_settings("HDMI-1", path=path), {"r": 1.0, "g": 0.6, "b": 0.35}
            )
            self.assertEqual(
                load_settings("eDP-1", path=path), {"r": 1.0, "g": 0.75, "b": 0.5}
            )

    def test_load_specific_monitor(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_settings(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            result = load_settings("HDMI-1", path=path)
            self.assertEqual(result, {"r": 1.0, "g": 0.85, "b": 0.65})

    def test_missing_monitor_returns_defaults(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_settings(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            result = load_settings("eDP-1", path=path)
            self.assertEqual(result, DEFAULTS)

    def test_missing_file_returns_defaults(self):
        result = load_settings("HDMI-1", path="/nonexistent/settings.json")
        self.assertEqual(result, DEFAULTS)

    def test_no_output_returns_defaults(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_settings(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            result = load_settings(None, path=path)
            self.assertEqual(result, DEFAULTS)

    def test_legacy_format_returns_values(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            with open(path, "w") as f:
                json.dump({"r": 1.0, "g": 0.85, "b": 0.65}, f)
            result = load_settings("HDMI-1", path=path)
            self.assertEqual(result, {"r": 1.0, "g": 0.85, "b": 0.65})

    def test_load_config_multi_monitor_format(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_settings(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            result = load_config(path=path)
            self.assertIn("monitors", result)
            self.assertIn("HDMI-1", result["monitors"])

    def test_roundtrip_multi_monitor(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_settings(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            save_settings(1.0, 0.75, 0.50, path=path, output="eDP-1")
            save_settings(1.0, 0.60, 0.35, path=path, output="DP-1")
            self.assertEqual(
                load_settings("HDMI-1", path=path), {"r": 1.0, "g": 0.85, "b": 0.65}
            )
            self.assertEqual(
                load_settings("eDP-1", path=path), {"r": 1.0, "g": 0.75, "b": 0.5}
            )
            self.assertEqual(
                load_settings("DP-1", path=path), {"r": 1.0, "g": 0.6, "b": 0.35}
            )


if __name__ == "__main__":
    unittest.main()
