"""Main GUI application for Blue Light Filter."""

import tkinter as tk
from constants import (BG, CARD, BORDER, FG, FG2, ACCENT, ACC2,
                       RED, GREEN, BLUE, DARK, MONO, MONO_B, MONO_S,
                       MONO_LG, PRESETS)
from xrandr_utils import get_connected_output, apply_gamma, build_command, has_xrandr
from color_utils import gamma_to_hex, warmth_label
from slider import Slider
from config import load_config, save_config


class App(tk.Tk):
    """Blue Light Filter GUI Application."""

    def __init__(self):
        super().__init__()
        self.title("Blue Light Filter")
        self.configure(bg=BG)
        self.resizable(False, False)

        self.output = get_connected_output()
        self.has_xr = has_xrandr()

        # Load saved settings or use defaults
        saved = load_config()
        self._r = saved.get('r', 1.00)
        self._g = saved.get('g', 0.85)
        self._b = saved.get('b', 0.65)

        self._build()

        # Auto-apply saved settings on startup
        if saved and self.has_xr and self.output:
            apply_gamma(self.output, self._r, self._g, self._b)

    # ── UI Construction ───────────────────────────────────────────────────────

    def _build(self):
        """Construct the entire UI."""
        self._build_header()
        self._sep()
        self._build_preview()
        self._build_display_info()
        self._sep()
        self._build_presets()
        self._sep()
        self._build_sliders()
        self._sep()
        self._build_command_box()
        self._build_buttons()
        self._build_status()
        self._refresh()

    def _build_header(self):
        """Build header with title."""
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=22, pady=(20, 2))
        tk.Label(hdr, text="BLUE LIGHT", font=MONO_LG, bg=BG, fg=FG).pack(side="left")
        tk.Label(hdr, text=" FILTER", font=MONO_LG, bg=BG, fg=ACCENT).pack(side="left")
        tk.Label(self, text="xrandr gamma control  -  Lubuntu / Openbox",
                 font=MONO_S, bg=BG, fg=FG2).pack(anchor="w", padx=22)

    def _build_preview(self):
        """Build color preview card."""
        pc = self._card()
        pi = tk.Frame(pc, bg=CARD)
        pi.pack(fill="x", padx=16, pady=14)

        self.swatch = tk.Canvas(pi, width=54, height=54, bg=CARD,
                                highlightthickness=0, bd=0)
        self.swatch.pack(side="left", padx=(0, 14))
        self._orb = self.swatch.create_oval(3, 3, 51, 51, fill="#ffcc88", outline="")

        mid = tk.Frame(pi, bg=CARD)
        mid.pack(side="left", fill="x", expand=True)
        tk.Label(mid, text="Screen Preview", font=MONO_B, bg=CARD, fg=FG).pack(anchor="w")
        self.vals_lbl = tk.Label(mid, text="", font=MONO_S, bg=CARD, fg=FG2)
        self.vals_lbl.pack(anchor="w")

        self.warm_lbl = tk.Label(pi, text="", font=MONO_B, bg=CARD, fg=ACCENT)
        self.warm_lbl.pack(side="right")

    def _build_display_info(self):
        """Build display detection info row."""
        dtxt = f"Display: {self.output}" if self.output else "  No display detected"
        dcol = GREEN if self.output else RED
        tk.Label(self, text=dtxt, font=MONO_S, bg=BG, fg=dcol
                 ).pack(anchor="w", padx=22, pady=(4, 0))

    def _build_presets(self):
        """Build preset buttons."""
        tk.Label(self, text="PRESETS", font=MONO_S, bg=BG, fg=FG2
                 ).pack(anchor="w", padx=22)
        pf = tk.Frame(self, bg=BG)
        pf.pack(fill="x", padx=22, pady=(6, 10))
        self._pbtns = []
        for i, (name, r, g, b) in enumerate(PRESETS):
            btn = tk.Button(pf, text=name, font=MONO_S,
                            bg=CARD, fg=FG2,
                            activebackground=BORDER, activeforeground=ACC2,
                            relief="flat", bd=0,
                            highlightthickness=1, highlightbackground=BORDER,
                            padx=8, pady=7, cursor="hand2",
                            command=lambda r=r, g=g, b=b, i=i: self._preset(r, g, b, i))
            btn.grid(row=0, column=i, padx=3, sticky="ew")
            pf.columnconfigure(i, weight=1)
            self._pbtns.append(btn)

    def _build_sliders(self):
        """Build RGB slider controls."""
        tk.Label(self, text="MANUAL CONTROL", font=MONO_S, bg=BG, fg=FG2
                 ).pack(anchor="w", padx=22)
        sc = self._card()
        self._sl_r, self._rl = self._slider_row(sc, "RED", RED, self._r)
        self._sl_g, self._gl = self._slider_row(sc, "GREEN", GREEN, self._g)
        self._sl_b, self._bl = self._slider_row(sc, "BLUE", BLUE, self._b)

    def _build_command_box(self):
        """Build command display box."""
        tk.Label(self, text="GENERATED COMMAND", font=MONO_S, bg=BG, fg=FG2
                 ).pack(anchor="w", padx=22)
        cc = tk.Frame(self, bg=DARK, highlightthickness=1, highlightbackground=BORDER)
        cc.pack(fill="x", padx=22, pady=(6, 4))
        ci = tk.Frame(cc, bg=DARK)
        ci.pack(fill="x", padx=14, pady=10)
        tk.Label(ci, text="$ ", font=MONO_B, bg=DARK, fg=ACCENT).pack(side="left", anchor="nw")
        self._cmd_lbl = tk.Label(ci, text="", font=MONO_S, bg=DARK,
                                  fg="#aaffcc", wraplength=400, justify="left")
        self._cmd_lbl.pack(side="left", fill="x", expand=True)

    def _build_buttons(self):
        """Build action buttons."""
        bf = tk.Frame(self, bg=BG)
        bf.pack(fill="x", padx=22, pady=(10, 6))
        tk.Button(bf, text="  Apply Now",
                  font=MONO_B, bg=ACCENT, fg="#1a0900",
                  activebackground=ACC2, activeforeground="#1a0900",
                  relief="flat", bd=0, padx=18, pady=10, cursor="hand2",
                  command=self._apply).pack(side="left", fill="x", expand=True, padx=(0, 6))
        tk.Button(bf, text="Save Permanently",
                  font=MONO_B, bg=CARD, fg=FG2,
                  activebackground=BORDER, activeforeground=FG,
                  relief="flat", bd=0,
                  highlightthickness=1, highlightbackground=BORDER,
                  padx=14, pady=10, cursor="hand2",
                  command=self._save_permanent).pack(side="left", padx=(0, 6))
        tk.Button(bf, text="Reset",
                  font=MONO_B, bg=CARD, fg=FG2,
                  activebackground=BORDER, activeforeground=FG,
                  relief="flat", bd=0,
                  highlightthickness=1, highlightbackground=BORDER,
                  padx=14, pady=10, cursor="hand2",
                  command=self._reset).pack(side="left", padx=(0, 6))
        tk.Button(bf, text="Copy CMD",
                  font=MONO_B, bg=CARD, fg=FG2,
                  activebackground=BORDER, activeforeground=FG,
                  relief="flat", bd=0,
                  highlightthickness=1, highlightbackground=BORDER,
                  padx=14, pady=10, cursor="hand2",
                  command=self._copy).pack(side="left")

    def _build_status(self):
        """Build status message label."""
        self._status = tk.Label(self, text="", font=MONO_S, bg=BG, fg=GREEN)
        self._status.pack(pady=(4, 16))

    def _sep(self):
        """Draw a separator line."""
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=22, pady=8)

    def _card(self):
        """Create a card container."""
        f = tk.Frame(self, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
        f.pack(fill="x", padx=22, pady=(4, 4))
        return f

    def _slider_row(self, parent, label, color, init):
        """Create a labeled slider row.

        Returns:
            tuple: (Slider widget, value label widget)
        """
        row = tk.Frame(parent, bg=CARD)
        row.pack(fill="x", padx=16, pady=(10, 4))
        top = tk.Frame(row, bg=CARD)
        top.pack(fill="x")
        tk.Label(top, text=label, font=MONO_B, bg=CARD,
                 fg=color, width=7, anchor="w").pack(side="left")
        val_lbl = tk.Label(top, text=f"{init:.2f}", font=MONO, bg=CARD, fg=FG2)
        val_lbl.pack(side="right")
        sl = Slider(row, from_=0.10, to=1.00, value=init,
                    thumb_color=color, bg=CARD,
                    on_change=lambda v, lbl=val_lbl: self._slider_moved(lbl, v))
        sl.pack(fill="x", pady=(6, 6))
        return sl, val_lbl

    # ── Callbacks ─────────────────────────────────────────────────────────────

    def _slider_moved(self, lbl, val):
        """Handle slider movement."""
        lbl.config(text=f"{val:.2f}")
        self._r = self._sl_r.get()
        self._g = self._sl_g.get()
        self._b = self._sl_b.get()
        for btn in self._pbtns:
            btn.config(bg=CARD, fg=FG2, highlightbackground=BORDER)
        self._refresh()

    def _refresh(self):
        """Update all UI elements to reflect current gamma values."""
        r, g, b = self._r, self._g, self._b
        self.swatch.itemconfig(self._orb, fill=gamma_to_hex(r, g, b))
        self.vals_lbl.config(text=f"R: {r:.2f}  G: {g:.2f}  B: {b:.2f}")
        self.warm_lbl.config(text=warmth_label(b))
        out = self.output or "<output>"
        self._cmd_lbl.config(text=build_command(out, r, g, b))

    def _preset(self, r, g, b, idx):
        """Apply a preset and highlight its button."""
        self._r, self._g, self._b = r, g, b
        self._sl_r.set(r)
        self._sl_g.set(g)
        self._sl_b.set(b)
        self._rl.config(text=f"{r:.2f}")
        self._gl.config(text=f"{g:.2f}")
        self._bl.config(text=f"{b:.2f}")
        for i, btn in enumerate(self._pbtns):
            if i == idx:
                btn.config(bg=ACCENT, fg="#1a0900", highlightbackground=ACCENT)
            else:
                btn.config(bg=CARD, fg=FG2, highlightbackground=BORDER)
        self._refresh()

    def _apply(self):
        """Apply filter to connected display."""
        if not self.has_xr:
            self._flash("  xrandr not found — install x11-xserver-utils", RED)
            return
        if not self.output:
            self._flash("  No connected display detected", RED)
            return
        apply_gamma(self.output, self._r, self._g, self._b)
        self._flash("  Filter applied to display!")

    def _reset(self):
        """Reset display to normal (no filter)."""
        self._preset(1.0, 1.0, 1.0, 0)
        if self.has_xr and self.output:
            apply_gamma(self.output, 1.0, 1.0, 1.0)
            self._flash("  Display reset to normal")

    def _copy(self):
        """Copy generated command to clipboard."""
        cmd = build_command(self.output or "<output>", self._r, self._g, self._b)
        self.clipboard_clear()
        self.clipboard_append(cmd)
        self._flash("  Command copied to clipboard!")

    def _save_permanent(self):
        """Save current gamma settings permanently."""
        if save_config(self._r, self._g, self._b):
            self._flash("  Settings saved permanently!", GREEN)
        else:
            self._flash("  Failed to save settings", RED)

    def _flash(self, msg, color=GREEN):
        """Show temporary status message."""
        self._status.config(text=msg, fg=color)
        self.after(2800, lambda: self._status.config(text=""))
