"""Tests for bluelight.config."""

import json
import tempfile
import unittest
from pathlib import Path
from bluelight.config import load_config, load_monitor_config, save_config


class TestSaveConfig(unittest.TestCase):

    def test_save_creates_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            result = save_config(1.0, 0.85, 0.65, path=path)
            self.assertTrue(result)
            self.assertTrue(path.exists())

    def test_save_writes_correct_values(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_config(1.0, 0.85, 0.65, path=path)
            with open(path) as f:
                data = json.load(f)
            self.assertEqual(data, {'r': 1.0, 'g': 0.85, 'b': 0.65})

    def test_save_rounds_values(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_config(0.999, 0.854, 0.651, path=path)
            with open(path) as f:
                data = json.load(f)
            self.assertEqual(data, {'r': 1.0, 'g': 0.85, 'b': 0.65})

    def test_save_creates_parent_dirs(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "sub" / "dir" / "settings.json"
            result = save_config(1.0, 1.0, 1.0, path=path)
            self.assertTrue(result)
            self.assertTrue(path.exists())


class TestLoadConfig(unittest.TestCase):

    def test_load_missing_file_returns_empty(self):
        result = load_config(path="/nonexistent/path/settings.json")
        self.assertEqual(result, {})

    def test_load_valid_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            with open(path, 'w') as f:
                json.dump({'r': 1.0, 'g': 0.85, 'b': 0.65}, f)
            result = load_config(path=path)
            self.assertEqual(result, {'r': 1.0, 'g': 0.85, 'b': 0.65})

    def test_load_corrupt_json_returns_empty(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            with open(path, 'w') as f:
                f.write("{broken json")
            result = load_config(path=path)
            self.assertEqual(result, {})

    def test_load_missing_keys_default_to_1(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            with open(path, 'w') as f:
                json.dump({'r': 0.5}, f)
            result = load_config(path=path)
            self.assertEqual(result, {'r': 0.5, 'g': 1.0, 'b': 1.0})

    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_config(1.0, 0.75, 0.50, path=path)
            result = load_config(path=path)
            self.assertEqual(result, {'r': 1.0, 'g': 0.75, 'b': 0.5})


class TestMultiMonitorConfig(unittest.TestCase):

    def test_save_per_monitor(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_config(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            with open(path) as f:
                data = json.load(f)
            self.assertIn('monitors', data)
            self.assertEqual(data['monitors']['HDMI-1'], {'r': 1.0, 'g': 0.85, 'b': 0.65})

    def test_save_multiple_monitors(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_config(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            save_config(1.0, 0.75, 0.50, path=path, output="eDP-1")
            with open(path) as f:
                data = json.load(f)
            self.assertEqual(data['monitors']['HDMI-1'], {'r': 1.0, 'g': 0.85, 'b': 0.65})
            self.assertEqual(data['monitors']['eDP-1'], {'r': 1.0, 'g': 0.75, 'b': 0.5})

    def test_save_overwrites_existing_monitor(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_config(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            save_config(1.0, 0.60, 0.35, path=path, output="HDMI-1")
            result = load_monitor_config("HDMI-1", path=path)
            self.assertEqual(result, {'r': 1.0, 'g': 0.6, 'b': 0.35})

    def test_save_preserves_other_monitors(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_config(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            save_config(1.0, 0.75, 0.50, path=path, output="eDP-1")
            save_config(1.0, 0.60, 0.35, path=path, output="HDMI-1")
            result_hdmi = load_monitor_config("HDMI-1", path=path)
            result_edp = load_monitor_config("eDP-1", path=path)
            self.assertEqual(result_hdmi, {'r': 1.0, 'g': 0.6, 'b': 0.35})
            self.assertEqual(result_edp, {'r': 1.0, 'g': 0.75, 'b': 0.5})

    def test_load_monitor_config(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_config(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            result = load_monitor_config("HDMI-1", path=path)
            self.assertEqual(result, {'r': 1.0, 'g': 0.85, 'b': 0.65})

    def test_load_monitor_config_missing_monitor(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_config(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            result = load_monitor_config("eDP-1", path=path)
            self.assertEqual(result, {})

    def test_load_monitor_config_missing_file(self):
        result = load_monitor_config("HDMI-1", path="/nonexistent/settings.json")
        self.assertEqual(result, {})

    def test_load_monitor_config_no_output(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_config(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            result = load_monitor_config(None, path=path)
            self.assertEqual(result, {})

    def test_load_monitor_config_legacy_format(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            with open(path, 'w') as f:
                json.dump({'r': 1.0, 'g': 0.85, 'b': 0.65}, f)
            result = load_monitor_config("HDMI-1", path=path)
            self.assertEqual(result, {'r': 1.0, 'g': 0.85, 'b': 0.65})

    def test_load_config_multi_monitor_format(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_config(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            result = load_config(path=path)
            self.assertIn('monitors', result)
            self.assertIn('HDMI-1', result['monitors'])

    def test_roundtrip_multi_monitor(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "settings.json"
            save_config(1.0, 0.85, 0.65, path=path, output="HDMI-1")
            save_config(1.0, 0.75, 0.50, path=path, output="eDP-1")
            save_config(1.0, 0.60, 0.35, path=path, output="DP-1")
            self.assertEqual(load_monitor_config("HDMI-1", path=path),
                             {'r': 1.0, 'g': 0.85, 'b': 0.65})
            self.assertEqual(load_monitor_config("eDP-1", path=path),
                             {'r': 1.0, 'g': 0.75, 'b': 0.5})
            self.assertEqual(load_monitor_config("DP-1", path=path),
                             {'r': 1.0, 'g': 0.6, 'b': 0.35})


if __name__ == "__main__":
    unittest.main()
