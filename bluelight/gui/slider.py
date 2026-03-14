"""Custom Canvas-based horizontal slider widget."""

import tkinter as tk
from bluelight.theme import CARD, BG


class Slider(tk.Canvas):
    """Smooth horizontal slider drawn entirely with Canvas."""

    def __init__(self, master, from_=0.0, to=1.0, value=1.0,
                 thumb_color="#ffffff", on_change=None, **kw):
        kw.setdefault("height", 24)
        kw.setdefault("bg", CARD)
        kw.setdefault("highlightthickness", 0)
        kw.setdefault("bd", 0)
        super().__init__(master, **kw)

        self.from_     = from_
        self.to        = to
        self._val      = value
        self.th_color  = thumb_color
        self.on_change = on_change

        self.bind("<Configure>",       self._draw)
        self.bind("<ButtonPress-1>",   self._click)
        self.bind("<B1-Motion>",       self._drag)
        self.bind("<ButtonRelease-1>", self._drag)

    def _draw(self, *_):
        """Draw slider track, fill, and thumb."""
        self.delete("all")
        w  = self.winfo_width()
        h  = self.winfo_height()
        if w < 4:
            return

        PAD = 11
        cy  = h // 2
        th  = 4
        rad = 9

        # track
        self.create_rectangle(PAD, cy-th//2, w-PAD, cy+th//2,
                               fill=CARD, outline="", width=0)
        # fill
        fx = PAD + int((self._val - self.from_) / (self.to - self.from_) * (w - 2*PAD))
        self.create_rectangle(PAD, cy-th//2, fx, cy+th//2,
                               fill=self.th_color, outline="", width=0)
        # thumb
        self.create_oval(fx-rad, cy-rad, fx+rad, cy+rad,
                          fill=self.th_color, outline=BG, width=2)

    def _px_to_val(self, x):
        """Convert pixel position to slider value."""
        PAD = 11
        w   = self.winfo_width()
        ratio = max(0.0, min(1.0, (x - PAD) / max(1, w - 2*PAD)))
        return round(self.from_ + ratio * (self.to - self.from_), 2)

    def _click(self, e):
        """Handle mouse click on slider."""
        self._set(self._px_to_val(e.x))

    def _drag(self, e):
        """Handle mouse drag on slider."""
        self._set(self._px_to_val(e.x))

    def _set(self, val):
        """Set slider value and trigger callback."""
        self._val = max(self.from_, min(self.to, val))
        self._draw()
        if self.on_change:
            self.on_change(self._val)

    def get(self):
        """Get current slider value."""
        return self._val

    def set(self, val):
        """Set slider value."""
        self._set(val)
