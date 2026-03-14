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

    @patch("bluelight.gui.app.load_config", return_value={})
    @patch("bluelight.gui.app.has_xrandr", return_value=True)
    @patch("bluelight.gui.app.get_connected_output", return_value="HDMI-1")
    @patch("bluelight.gui.app.apply_gamma")
    @patch("bluelight.gui.app.tk.Tk.__init__", return_value=None)
    def test_apply_calls_gamma(self, mock_tk, mock_apply, mock_out, mock_xr, mock_cfg):
        from bluelight.gui.app import App
        app = App.__new__(App)
        app.output = "HDMI-1"
        app.has_xr = True
        app._r, app._g, app._b = 1.0, 0.85, 0.65
        app._status = MagicMock()
        app.after = MagicMock()
        app._apply()
        mock_apply.assert_called_once_with("HDMI-1", 1.0, 0.85, 0.65)

    @patch("bluelight.gui.app.apply_gamma")
    def test_apply_blocked_without_xrandr(self, mock_apply):
        from bluelight.gui.app import App
        app = App.__new__(App)
        app.output = "HDMI-1"
        app.has_xr = False
        app._status = MagicMock()
        app.after = MagicMock()
        app._apply()
        mock_apply.assert_not_called()

    @patch("bluelight.gui.app.apply_gamma")
    def test_apply_blocked_without_output(self, mock_apply):
        from bluelight.gui.app import App
        app = App.__new__(App)
        app.output = None
        app.has_xr = True
        app._status = MagicMock()
        app.after = MagicMock()
        app._apply()
        mock_apply.assert_not_called()

    @patch("bluelight.gui.app.save_config", return_value=True)
    def test_save_permanent_success(self, mock_save):
        from bluelight.gui.app import App
        app = App.__new__(App)
        app._r, app._g, app._b = 1.0, 0.85, 0.65
        app._status = MagicMock()
        app.after = MagicMock()
        app._save_permanent()
        mock_save.assert_called_once_with(1.0, 0.85, 0.65)

    @patch("bluelight.gui.app.build_command", return_value="xrandr --output HDMI-1 --gamma 1.00:0.85:0.65")
    def test_copy_to_clipboard(self, mock_cmd):
        from bluelight.gui.app import App
        app = App.__new__(App)
        app.output = "HDMI-1"
        app._r, app._g, app._b = 1.0, 0.85, 0.65
        app._status = MagicMock()
        app.after = MagicMock()
        app.clipboard_clear = MagicMock()
        app.clipboard_append = MagicMock()
        app._copy()
        app.clipboard_append.assert_called_once_with("xrandr --output HDMI-1 --gamma 1.00:0.85:0.65")


if __name__ == "__main__":
    unittest.main()
