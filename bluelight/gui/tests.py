"""Tests for bluelight.gui (slider + app)."""

import unittest
from unittest.mock import patch, MagicMock


class TestSliderLogic(unittest.TestCase):
    """Test Slider value logic without rendering."""

    @patch("bluelight.gui.slider.tk.Canvas.__init__", return_value=None)
    @patch("bluelight.gui.slider.tk.Canvas.bind")
    def _make_slider(self, from_, to, value, mock_bind, mock_init):
        from bluelight.gui.slider import Slider
        s = Slider.__new__(Slider)
        s.from_ = from_
        s.to = to
        s._val = value
        s.th_color = "#ff0000"
        s.on_change = None
        return s

    def test_get_returns_value(self):
        s = self._make_slider(0.0, 1.0, 0.5)
        self.assertEqual(s.get(), 0.5)

    def test_set_clamps_above_max(self):
        s = self._make_slider(0.0, 1.0, 0.5)
        s._draw = MagicMock()
        s._set(1.5)
        self.assertEqual(s._val, 1.0)

    def test_set_clamps_below_min(self):
        s = self._make_slider(0.1, 1.0, 0.5)
        s._draw = MagicMock()
        s._set(-0.5)
        self.assertEqual(s._val, 0.1)

    def test_set_triggers_callback(self):
        s = self._make_slider(0.0, 1.0, 0.5)
        s._draw = MagicMock()
        cb = MagicMock()
        s.on_change = cb
        s._set(0.7)
        cb.assert_called_once_with(0.7)

    def test_set_no_callback_if_none(self):
        s = self._make_slider(0.0, 1.0, 0.5)
        s._draw = MagicMock()
        s.on_change = None
        s._set(0.7)  # should not raise


class TestAppCallbacks(unittest.TestCase):
    """Test App callback logic with mocked display."""

    def _make_app(self, outputs=None, has_xr=True, gamma=None):
        """Create an App instance with mocked internals."""
        from bluelight.gui.app import App
        app = App.__new__(App)
        app.outputs = outputs or ["HDMI-1"]
        app.has_xr = has_xr
        app._monitor_gamma = gamma or {"HDMI-1": (1.0, 0.85, 0.65)}
        app._r, app._g, app._b = 1.0, 0.85, 0.65
        app._status = MagicMock()
        app.after = MagicMock()

        import tkinter as tk
        app._selected = MagicMock()
        app._selected.get.return_value = app.outputs[0] if app.outputs else ""
        return app

    @patch("bluelight.gui.app.apply_gamma")
    def test_apply_calls_gamma(self, mock_apply):
        app = self._make_app()
        app._apply()
        mock_apply.assert_called_once_with("HDMI-1", 1.0, 0.85, 0.65)

    @patch("bluelight.gui.app.apply_gamma")
    def test_apply_all_monitors(self, mock_apply):
        app = self._make_app(
            outputs=["HDMI-1", "eDP-1"],
            gamma={"HDMI-1": (1.0, 0.85, 0.65), "eDP-1": (1.0, 0.75, 0.50)})
        app._selected.get.return_value = "All Monitors"
        app._apply()
        self.assertEqual(mock_apply.call_count, 2)

    @patch("bluelight.gui.app.apply_gamma")
    def test_apply_blocked_without_xrandr(self, mock_apply):
        app = self._make_app(has_xr=False)
        app._apply()
        mock_apply.assert_not_called()

    @patch("bluelight.gui.app.apply_gamma")
    def test_apply_blocked_without_output(self, mock_apply):
        app = self._make_app(outputs=[])
        app._selected.get.return_value = ""
        app._monitor_gamma = {}
        app._apply()
        mock_apply.assert_not_called()

    @patch("bluelight.gui.app.save_config", return_value=True)
    def test_save_permanent_per_monitor(self, mock_save):
        app = self._make_app()
        app._save_permanent()
        mock_save.assert_called_once_with(1.0, 0.85, 0.65, output="HDMI-1")

    @patch("bluelight.gui.app.build_command", return_value="xrandr --output HDMI-1 --gamma 1.00:0.85:0.65")
    def test_copy_to_clipboard(self, mock_cmd):
        app = self._make_app()
        app.clipboard_clear = MagicMock()
        app.clipboard_append = MagicMock()
        app._copy()
        app.clipboard_append.assert_called_once()

    @patch("bluelight.gui.app.apply_gamma")
    def test_apply_single_monitor_from_multi(self, mock_apply):
        """Selecting one monitor only applies to that monitor."""
        app = self._make_app(
            outputs=["HDMI-1", "eDP-1"],
            gamma={"HDMI-1": (1.0, 0.85, 0.65), "eDP-1": (1.0, 0.75, 0.50)})
        app._selected.get.return_value = "eDP-1"
        app._apply()
        mock_apply.assert_called_once_with("eDP-1", 1.0, 0.75, 0.50)

    @patch("bluelight.gui.app.apply_gamma")
    def test_apply_all_monitors_uses_per_monitor_gamma(self, mock_apply):
        """All Monitors applies each monitor's own stored gamma."""
        app = self._make_app(
            outputs=["HDMI-1", "eDP-1"],
            gamma={"HDMI-1": (1.0, 0.85, 0.65), "eDP-1": (1.0, 0.75, 0.50)})
        app._selected.get.return_value = "All Monitors"
        app._apply()
        calls = mock_apply.call_args_list
        self.assertEqual(calls[0], (("HDMI-1", 1.0, 0.85, 0.65),))
        self.assertEqual(calls[1], (("eDP-1", 1.0, 0.75, 0.50),))

    @patch("bluelight.gui.app.apply_gamma")
    def test_reset_resets_all_targeted(self, mock_apply):
        """Reset applies 1.0/1.0/1.0 to all targeted monitors."""
        app = self._make_app(
            outputs=["HDMI-1", "eDP-1"],
            gamma={"HDMI-1": (1.0, 0.85, 0.65), "eDP-1": (1.0, 0.75, 0.50)})
        app._selected.get.return_value = "All Monitors"
        app._pbtns = [MagicMock() for _ in range(5)]
        app._sl_r = MagicMock(get=MagicMock(return_value=1.0))
        app._sl_g = MagicMock(get=MagicMock(return_value=1.0))
        app._sl_b = MagicMock(get=MagicMock(return_value=1.0))
        app._rl = MagicMock()
        app._gl = MagicMock()
        app._bl = MagicMock()
        app.swatch = MagicMock()
        app._orb = "orb"
        app.vals_lbl = MagicMock()
        app.warm_lbl = MagicMock()
        app._cmd_lbl = MagicMock()
        app._reset()
        # Should have called apply_gamma with 1.0 for both monitors
        reset_calls = [c for c in mock_apply.call_args_list
                       if c == (("HDMI-1", 1.0, 1.0, 1.0),)
                       or c == (("eDP-1", 1.0, 1.0, 1.0),)]
        self.assertEqual(len(reset_calls), 2)

    @patch("bluelight.gui.app.save_config", return_value=True)
    def test_save_permanent_all_monitors(self, mock_save):
        """Save permanently saves each monitor's gamma individually."""
        app = self._make_app(
            outputs=["HDMI-1", "eDP-1"],
            gamma={"HDMI-1": (1.0, 0.85, 0.65), "eDP-1": (1.0, 0.75, 0.50)})
        app._selected.get.return_value = "All Monitors"
        app._save_permanent()
        calls = mock_save.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0], ((1.0, 0.85, 0.65,), {"output": "HDMI-1"}))
        self.assertEqual(calls[1], ((1.0, 0.75, 0.50,), {"output": "eDP-1"}))

    def test_target_outputs_single(self):
        """_target_outputs returns single monitor when one is selected."""
        app = self._make_app(outputs=["HDMI-1", "eDP-1"])
        app._selected.get.return_value = "HDMI-1"
        self.assertEqual(app._target_outputs(), ["HDMI-1"])

    def test_target_outputs_all(self):
        """_target_outputs returns all monitors when All Monitors is selected."""
        app = self._make_app(outputs=["HDMI-1", "eDP-1"])
        app._selected.get.return_value = "All Monitors"
        self.assertEqual(app._target_outputs(), ["HDMI-1", "eDP-1"])

    def test_target_outputs_empty(self):
        """_target_outputs returns empty list when no selection."""
        app = self._make_app(outputs=[])
        app._selected.get.return_value = ""
        self.assertEqual(app._target_outputs(), [])

    def test_current_rgb_specific_monitor(self):
        """_current_rgb returns the selected monitor's gamma."""
        app = self._make_app(
            outputs=["HDMI-1", "eDP-1"],
            gamma={"HDMI-1": (1.0, 0.85, 0.65), "eDP-1": (1.0, 0.75, 0.50)})
        app._selected.get.return_value = "eDP-1"
        self.assertEqual(app._current_rgb(), (1.0, 0.75, 0.50))

    def test_current_rgb_all_monitors(self):
        """_current_rgb returns first monitor's gamma for All Monitors."""
        app = self._make_app(
            outputs=["HDMI-1", "eDP-1"],
            gamma={"HDMI-1": (1.0, 0.85, 0.65), "eDP-1": (1.0, 0.75, 0.50)})
        app._selected.get.return_value = "All Monitors"
        self.assertEqual(app._current_rgb(), (1.0, 0.85, 0.65))

    @patch("bluelight.gui.app.build_command", side_effect=lambda out, r, g, b: f"xrandr --output {out} --gamma {r:.2f}:{g:.2f}:{b:.2f}")
    def test_copy_all_monitors_multiple_commands(self, mock_cmd):
        """Copy with All Monitors produces one command per monitor."""
        app = self._make_app(
            outputs=["HDMI-1", "eDP-1"],
            gamma={"HDMI-1": (1.0, 0.85, 0.65), "eDP-1": (1.0, 0.75, 0.50)})
        app._selected.get.return_value = "All Monitors"
        app.clipboard_clear = MagicMock()
        app.clipboard_append = MagicMock()
        app._copy()
        text = app.clipboard_append.call_args[0][0]
        self.assertIn("HDMI-1", text)
        self.assertIn("eDP-1", text)
        self.assertEqual(text.count("xrandr"), 2)


if __name__ == "__main__":
    unittest.main()
