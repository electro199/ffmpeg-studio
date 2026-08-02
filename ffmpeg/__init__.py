"""
Pythonic FFmpeg wrapper for building and running commands, including complex filter graphs.

This module provides a Pythonic interface to FFmpeg, letting you construct and execute
FFmpeg commands programmatically — video/audio conversion, filtering, and transcoding —
without hand-writing raw shell commands or filter_complex strings.

Requirements:
- FFmpeg must be installed and accessible on the system PATH.
"""

from .inputs import (
    InputFile,
    FileInputOptions,
    VideoFile,
    ImageFile,
    AudioFile,
    VirtualVideo,
)
from .filters import apply, apply2
from .output.output import Map, OutFile
from .ffmpeg import FFmpeg, export
from .utils.diagram import draw_filter_graph
from .exception import FFmpegException, FFprobeException
from . import inputs, filters, output, exception, ffplay, ffprobe
import logging

logger = logging.getLogger("ffmpeg")


__version__ = "0.1.4"

__all__ = [
    "InputFile",
    "FileInputOptions",
    "VideoFile",
    "ImageFile",
    "AudioFile",
    "VirtualVideo",
    "apply",
    "apply2",
    "Map",
    "OutFile",
    "FFmpeg",
    "export",
    "draw_filter_graph",
    "FFmpegException",
    "FFprobeException",
    "inputs",
    "filters",
    "exception",
    "ffplay",
    "ffprobe",
    "__version__",
]
