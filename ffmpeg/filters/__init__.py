"""
This module contains various FFmpeg filters as Python classes.
The filters Always Inherit from BaseFilter class and Optionally TimelineEditingMixin if they support timeline editing.

"""

from .adelay import AudioDelay
from .amix import AudioMix
from .apply_filter import apply, apply2
from .base import BaseFilter
from .concat import Concat
from .crop import Crop
from .delogo import Delogo
from .draw_box import Box
from .draw_text import Text
from .hstack import HorizontalStack
from .mixins.enable import TimelineEditingMixin
from .overlay import Overlay
from .sar import SetSampleAspectRatio
from .scale import (
    AspectRatioMode,
    ColorMatrix,
    EvalMode,
    Intent,
    InterlacingMode,
    IOChromaLocation,
    IOPrimaries,
    IORange,
    Scale,
)
from .split import Split
from .subtitles import Subtitles
from .timebase import SetTimeBase
from .volume import Volume
from .vstack import VerticalStack
from .xfade import XFade
from .format import Format
from .aformat import AudioFormat

__all__ = [
    # util
    "apply",
    "apply2",
    # video
    "Scale",
    "EvalMode",
    "AspectRatioMode",
    "ColorMatrix",
    "Intent",
    "InterlacingMode",
    "IOChromaLocation",
    "IOPrimaries",
    "IORange",
    "Box",
    "Text",
    "Overlay",
    "XFade",
    "Subtitles",
    "SetTimeBase",
    "SetSampleAspectRatio",
    "VerticalStack",
    "HorizontalStack",
    "Crop",
    "Delogo",
    # audio
    "AudioMix",
    "AudioFormat",
    "Volume",
    "AudioDelay",
    # general
    "Concat",
    "Format",
    "Split",
    # internal
    "BaseFilter",
    "TimelineEditingMixin",
]
