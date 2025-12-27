import subprocess
import json
from typing import Any, Iterable, Optional
from ..exception.exceptions import FFprobeException


def ffprobe(
    file_path: str,
    options: Optional[Iterable[str]] = None,
) -> Any:
    """
    Run ffprobe with the given options on the specified file.

    Args:
        file_path: Path to the media file.
        options: set ffprobe options (default extracts streams and format).

    Returns:
        Parsed JSON dictionary output.
    """
    flags = []
    if not options:
        flags.extend(
            (
                "-show_streams",
                "-show_format",
            )
        )
    else:
        flags.extend(options)

    flags.extend(
        (
            "-print_format",
            "json",
        )
    )

    cmd = [f"ffprobe", *flags, file_path]
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise FFprobeException(msg=result.stderr, return_code=result.returncode)

    return json.loads(result.stdout)
