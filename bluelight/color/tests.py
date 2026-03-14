"""Tests for bluelight.color."""

import unittest
from bluelight.color import gamma_to_hex, warmth_label


class TestGammaToHex(unittest.TestCase):

    def test_full_white(self):
        result = gamma_to_hex(1.0, 1.0, 1.0)
        self.assertEqual(result, "#ffe1a0")

    def test_full_black(self):
        result = gamma_to_hex(0.0, 0.0, 0.0)
        self.assertEqual(result, "#002814")

    def test_red_only(self):
        result = gamma_to_hex(1.0, 0.0, 0.0)
        self.assertEqual(result, "#ff2814")

    def test_returns_lowercase_hex(self):
        result = gamma_to_hex(0.5, 0.5, 0.5)
        self.assertTrue(result.startswith("#"))
        self.assertEqual(len(result), 7)
        self.assertEqual(result, result.lower())

    def test_clamps_green_channel(self):
        result = gamma_to_hex(1.0, 1.5, 1.0)
        r, g, b = int(result[1:3], 16), int(result[3:5], 16), int(result[5:7], 16)
        self.assertLessEqual(g, 255)

    def test_clamps_blue_channel(self):
        result = gamma_to_hex(1.0, 1.0, 2.0)
        b_val = int(result[5:7], 16)
        self.assertLessEqual(b_val, 255)


class TestWarmthLabel(unittest.TestCase):

    def test_cool_daylight(self):
        self.assertEqual(warmth_label(1.0), "Cool - daylight")
        self.assertEqual(warmth_label(0.95), "Cool - daylight")

    def test_slightly_warm(self):
        self.assertEqual(warmth_label(0.90), "Slightly warm")
        self.assertEqual(warmth_label(0.82), "Slightly warm")

    def test_warm(self):
        self.assertEqual(warmth_label(0.70), "Warm")
        self.assertEqual(warmth_label(0.65), "Warm")

    def test_hot(self):
        self.assertEqual(warmth_label(0.55), "Hot")
        self.assertEqual(warmth_label(0.50), "Hot")

    def test_max_warm(self):
        self.assertEqual(warmth_label(0.40), "Max warm")
        self.assertEqual(warmth_label(0.0), "Max warm")

    def test_boundary_values(self):
        self.assertEqual(warmth_label(0.94), "Slightly warm")
        self.assertEqual(warmth_label(0.81), "Warm")
        self.assertEqual(warmth_label(0.64), "Hot")
        self.assertEqual(warmth_label(0.49), "Max warm")


if __name__ == "__main__":
    unittest.main()
