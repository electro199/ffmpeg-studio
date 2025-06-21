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
    """Generate flags"""
    flags = []

    for k, v in kwflags.items():
        flags.append(f"-{k}")
        flags.append(str(v))

    return flags


def build_name_kvargs_format(name: str, flags: dict) -> str:
    s = []
    for k, v in flags.items():
        if v is None:
            continue
        elif isinstance(v, bool):
            v = int(v)

        s.append(f"{k}={v}")

    return f"{name}=" + (":".join(s))
