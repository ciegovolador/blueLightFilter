#!/usr/bin/env python3
"""
Blue Light Filter GUI for Lubuntu — xrandr gamma control
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Zero external dependencies — uses only Python stdlib.
tkinter ships with Python on Lubuntu — no pip install needed.

Run:  python3 main.py

If tkinter is missing (rare):  sudo apt install python3-tk
"""

from bluelight import App


if __name__ == "__main__":
    App().mainloop()
