"""xrandr display control utilities."""

import subprocess
import shutil


def get_connected_output():
    """Detect the connected display output name.

    Returns:
        str or None: Output name (e.g., "HDMI-1") or None if not found.
    """
    try:
        out = subprocess.check_output(["xrandr"], text=True, stderr=subprocess.DEVNULL)
        for line in out.splitlines():
            if " connected" in line:
                return line.split()[0]
    except Exception:
        pass
    return None


def apply_gamma(output, r, g, b):
    """Apply gamma adjustment to display.

    Args:
        output (str): Display output name.
        r (float): Red gamma value (0.0-1.0).
        g (float): Green gamma value (0.0-1.0).
        b (float): Blue gamma value (0.0-1.0).
    """
    subprocess.Popen(
        ["xrandr", "--output", output, "--gamma", f"{r:.2f}:{g:.2f}:{b:.2f}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def build_command(output, r, g, b):
    """Generate xrandr command string.

    Args:
        output (str): Display output name.
        r (float): Red gamma value.
        g (float): Green gamma value.
        b (float): Blue gamma value.

    Returns:
        str: xrandr command string.
    """
    return f"xrandr --output {output} --gamma {r:.2f}:{g:.2f}:{b:.2f}"


def has_xrandr():
    """Check if xrandr is available.

    Returns:
        bool: True if xrandr is installed.
    """
    return shutil.which("xrandr") is not None
