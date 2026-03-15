"""xrandr display control utilities."""

import subprocess
import shutil


def get_connected_outputs():
    """Detect all connected display output names.

    Returns:
        list[str]: Output names (e.g., ["HDMI-1", "eDP-1"]), empty if none found.
    """
    outputs = []
    try:
        out = subprocess.check_output(["xrandr"], text=True, stderr=subprocess.DEVNULL)
        for line in out.splitlines():
            if " connected" in line:
                outputs.append(line.split()[0])
    except Exception:
        pass
    return outputs


def apply_gamma(output, r, g, b):
    """Apply gamma adjustment to display."""
    cmd = build_command(output, r, g, b).split()
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def build_command(output, r, g, b):
    """Generate xrandr command string."""
    return f"xrandr --output {output} --gamma {r:.2f}:{g:.2f}:{b:.2f}"


def has_xrandr():
    """Check if xrandr is available."""
    return shutil.which("xrandr") is not None
