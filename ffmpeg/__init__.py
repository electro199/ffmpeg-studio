"""
FFmpeg Wrapper for Python

This module provides a Pythonic interface to FFmpeg, allowing users to construct and execute FFmpeg commands programmatically.
It simplifies video and audio processing tasks such as format conversion, filtering, and transcoding.


Requirements:
- FFmpeg must be installed and accessible via the system path.

"""

from . import inputs, filters, exception, ffplay, ffprobe
from .output import output

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


import logging

logger = logging.getLogger("ffmpeg")


__version__ = "0.0.15"
