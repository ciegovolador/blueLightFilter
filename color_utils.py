"""Color conversion and warmth labeling utilities."""


def gamma_to_hex(r, g, b):
    """Convert RGB gamma values to hex color.

    Args:
        r (float): Red gamma value (0.0-1.0).
        g (float): Green gamma value (0.0-1.0).
        b (float): Blue gamma value (0.0-1.0).

    Returns:
        str: Hex color string (e.g., "#ff9944").
    """
    ri = int(255 * r)
    gi = int(min(255, 185 * g + 40))
    bi = int(min(255, 140 * b + 20))
    return f"#{ri:02x}{gi:02x}{bi:02x}"


def warmth_label(b):
    """Get human-readable warmth label based on blue channel value.

    Args:
        b (float): Blue gamma value (0.0-1.0).

    Returns:
        str: Warmth label.
    """
    if b >= 0.95:
        return "Cool - daylight"
    if b >= 0.82:
        return "Slightly warm"
    if b >= 0.65:
        return "Warm"
    if b >= 0.50:
        return "Hot"
    return "Max warm"
