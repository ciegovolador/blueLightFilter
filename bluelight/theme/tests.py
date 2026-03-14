"""Tests for bluelight.theme."""

import unittest
from bluelight.theme import (
    BG, CARD, BORDER, FG, FG2, ACCENT, ACC2,
    RED, GREEN, BLUE, DARK,
    MONO, MONO_B, MONO_S, MONO_LG,
    PRESETS,
)


class TestColors(unittest.TestCase):

    def test_all_colors_are_hex(self):
        for color in (BG, CARD, BORDER, FG, FG2, ACCENT, ACC2, RED, GREEN, BLUE, DARK):
            self.assertTrue(color.startswith("#"), f"{color} is not hex")
            self.assertEqual(len(color), 7, f"{color} is not 7 chars")

    def test_colors_are_lowercase(self):
        for color in (BG, CARD, BORDER, FG, FG2, ACCENT, ACC2, RED, GREEN, BLUE, DARK):
            self.assertEqual(color, color.lower())


class TestFonts(unittest.TestCase):

    def test_mono_is_tuple(self):
        for font in (MONO, MONO_B, MONO_S, MONO_LG):
            self.assertIsInstance(font, tuple)
            self.assertGreaterEqual(len(font), 2)

    def test_mono_family(self):
        for font in (MONO, MONO_B, MONO_S, MONO_LG):
            self.assertEqual(font[0], "Courier New")


class TestPresets(unittest.TestCase):

    def test_presets_is_list(self):
        self.assertIsInstance(PRESETS, list)
        self.assertGreater(len(PRESETS), 0)

    def test_preset_structure(self):
        for name, r, g, b in PRESETS:
            self.assertIsInstance(name, str)
            self.assertIsInstance(r, float)
            self.assertIsInstance(g, float)
            self.assertIsInstance(b, float)

    def test_preset_values_in_range(self):
        for name, r, g, b in PRESETS:
            for val in (r, g, b):
                self.assertGreaterEqual(val, 0.0, f"{name}: value {val} < 0")
                self.assertLessEqual(val, 1.0, f"{name}: value {val} > 1")

    def test_first_preset_is_daylight(self):
        name, r, g, b = PRESETS[0]
        self.assertEqual(name, "Daylight")
        self.assertEqual((r, g, b), (1.0, 1.0, 1.0))


if __name__ == "__main__":
    unittest.main()
