"""Slider widget with colored fill (Canvas) + native interaction (Scale)."""

import tkinter as tk
from bluelight.constants import CARD, BG


class Slider(tk.Frame):
    """Hybrid slider: Canvas for colored fill, Scale for native interaction."""

    def __init__(
        self,
        master,
        from_=0.0,
        to=1.0,
        value=1.0,
        thumb_color="#ffffff",
        on_change=None,
        **kw,
    ):
        kw.setdefault("bg", CARD)
        super().__init__(master, **kw)

        self.from_ = from_
        self.to = to
        self._val = value
        self.th_color = thumb_color
        self.on_change = on_change

        # Colored fill bar
        self._fill = tk.Canvas(self, height=6, bg=BG, highlightthickness=0, bd=0)
        self._fill.pack(fill="x", pady=(4, 0))
        self._fill.bind("<Configure>", lambda e: self._draw_fill())

        # Native Scale for interaction
        self._scale = tk.Scale(
            self,
            from_=from_,
            to=to,
            orient="horizontal",
            resolution=0.01,
            showvalue=0,
            sliderlength=18,
            bg=CARD,
            fg=thumb_color,
            troughcolor=BG,
            activebackground=thumb_color,
            highlightthickness=0,
            bd=0,
            command=self._on_scale,
        )
        self._scale.pack(fill="x")
        self._scale.set(value)

    def _on_scale(self, val):
        """Handle Scale value change."""
        self._val = float(val)
        self._draw_fill()
        if self.on_change:
            self.on_change(self._val)

    def _draw_fill(self):
        """Redraw the colored fill bar proportional to current value."""
        self._fill.delete("all")
        w = self._fill.winfo_width()
        if w < 4:
            return
        ratio = (self._val - self.from_) / (self.to - self.from_)
        ratio = max(0.0, min(1.0, ratio))
        self._fill.create_rectangle(
            0, 0, int(w * ratio), 6, fill=self.th_color, width=0
        )

    def get(self):
        """Get current slider value."""
        return self._val

    def set(self, val):
        """Set slider value programmatically."""
        self._val = val
        self._scale.set(val)
        self._draw_fill()
