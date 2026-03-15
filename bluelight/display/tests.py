"""Tests for bluelight.display."""

import unittest
from unittest.mock import patch
from bluelight.display import (
    build_command, get_connected_outputs, has_xrandr, apply_gamma
)


class TestBuildCommand(unittest.TestCase):

    def test_basic_command(self):
        result = build_command("HDMI-1", 1.0, 0.85, 0.65)
        self.assertEqual(result, "xrandr --output HDMI-1 --gamma 1.00:0.85:0.65")

    def test_different_output(self):
        result = build_command("eDP-1", 1.0, 1.0, 1.0)
        self.assertEqual(result, "xrandr --output eDP-1 --gamma 1.00:1.00:1.00")


class TestGetConnectedOutputs(unittest.TestCase):

    @patch("bluelight.display.subprocess.check_output")
    def test_detects_multiple_displays(self, mock_out):
        mock_out.return_value = (
            "HDMI-1 connected 1920x1080+0+0\n"
            "VGA-1 disconnected\n"
            "eDP-1 connected 1366x768+1920+0\n"
        )
        self.assertEqual(get_connected_outputs(), ["HDMI-1", "eDP-1"])

    @patch("bluelight.display.subprocess.check_output")
    def test_single_display(self, mock_out):
        mock_out.return_value = "HDMI-1 connected 1920x1080+0+0\n"
        self.assertEqual(get_connected_outputs(), ["HDMI-1"])

    @patch("bluelight.display.subprocess.check_output")
    def test_three_displays(self, mock_out):
        mock_out.return_value = (
            "HDMI-1 connected 1920x1080+0+0\n"
            "DP-1 connected 2560x1440+1920+0\n"
            "VGA-1 disconnected\n"
            "eDP-1 connected 1366x768+4480+0\n"
        )
        self.assertEqual(get_connected_outputs(), ["HDMI-1", "DP-1", "eDP-1"])

    @patch("bluelight.display.subprocess.check_output")
    def test_preserves_order(self, mock_out):
        mock_out.return_value = (
            "eDP-1 connected 1366x768+0+0\n"
            "HDMI-1 connected 1920x1080+1366+0\n"
        )
        self.assertEqual(get_connected_outputs(), ["eDP-1", "HDMI-1"])

    @patch("bluelight.display.subprocess.check_output")
    def test_no_connected_displays(self, mock_out):
        mock_out.return_value = "VGA-1 disconnected\n"
        self.assertEqual(get_connected_outputs(), [])

    @patch("bluelight.display.subprocess.check_output", side_effect=FileNotFoundError)
    def test_xrandr_missing(self, mock_out):
        self.assertEqual(get_connected_outputs(), [])

class TestHasXrandr(unittest.TestCase):

    @patch("bluelight.display.shutil.which", return_value="/usr/bin/xrandr")
    def test_xrandr_installed(self, mock_which):
        self.assertTrue(has_xrandr())

    @patch("bluelight.display.shutil.which", return_value=None)
    def test_xrandr_not_installed(self, mock_which):
        self.assertFalse(has_xrandr())


class TestApplyGamma(unittest.TestCase):

    @patch("bluelight.display.subprocess.Popen")
    def test_calls_xrandr(self, mock_popen):
        apply_gamma("HDMI-1", 1.0, 0.85, 0.65)
        mock_popen.assert_called_once()
        args = mock_popen.call_args[0][0]
        self.assertEqual(args, ["xrandr", "--output", "HDMI-1", "--gamma", "1.00:0.85:0.65"])


if __name__ == "__main__":
    unittest.main()
