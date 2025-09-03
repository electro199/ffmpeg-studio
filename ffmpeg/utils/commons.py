"""
common functions used by ffmpeg-studio feel free to use them!

"""

from typing import Any


def wrap_quotes(text: str) -> str:
    return '"' + text + '"'


def wrap_sqrtbrkt(text: str) -> str:
    return "[" + str(text) + "]"


def parse_value(value):
    """Convert FFmpeg progress values to appropriate data types."""

    if value == "N/A":
        return None

    if value.isdigit():
        return int(value)

    try:
        return float(value)
    except ValueError:
        return value


def build_flags(kwflags: dict[str, Any]) -> list[str]:
    """
    Generate flags for FFmpeg command from key-value pairs.
    if value is bool, convert to int (True=1, False=0)
    if value is None, skip the flag value part (y=None, ["-y"]).

    Args:
        kwflags (dict): Dictionary of key-value pairs representing flags.

    Returns:
        list: List of command-line flags for FFmpeg.
    """
    flags = []

    for k, v in kwflags.items():
        flags.append(f"-{k}")

        if v is None:
            continue
        elif isinstance(v, bool):
            v = int(v)

        flags.append(str(v))

    return flags


def build_name_kvargs_format(name: str, flags: dict) -> str:
    """
    Build a formatted string for FFmpeg filter options. Automatically skips None values and converts bool int.
    Args:
        name (str): The name of the filter.
        flags (dict): A dictionary of key-value pairs representing filter options.

    Example:
        ```python
        build_name_kvargs_format("scale", {"w": 1280, "h": 720, "force_original_aspect_ratio": "decrease"})
        returns "scale=w=1280:h=720:force_original_aspect_ratio=decrease"
        ```
    """

    s = []
    for k, v in flags.items():
        if v is None:
            continue
        elif isinstance(v, bool):
            v = int(v)

        s.append(f"{k}={v}")

    return f"{name}=" + (":".join(s))
