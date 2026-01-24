"""
FFmpeg Wrapper for Python

This module provides a Pythonic interface to FFmpeg, allowing users to construct and execute FFmpeg commands programmatically.
It simplifies video and audio processing tasks such as format conversion, filtering, and transcoding.


Requirements:
- FFmpeg must be installed and accessible via the system path.

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


__version__ = "0.1.2"

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

