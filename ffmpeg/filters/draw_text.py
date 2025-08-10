import os
from typing import Optional, Any
from .base import BaseFilter
from .mixins.enable import TimelineEditingMixin


class Text(BaseFilter, TimelineEditingMixin):
    """
    Draw text using FFmpeg's `drawtext` filter.
    Most common args in __init__, others via builder methods.
    """

    def __init__(
        self,
        text: str,
        x: int | str,
        y: int | str,
        fontsize: int = 16,
        fontname: str = "arial.ttf",
        color: str = "white",
        alpha: Optional[float] = None,
        **kwargs,
    ):
        super().__init__("drawtext")

        self.text_expansion_flag = False
        flags = {
            "text": self.escape_arguments(text),
            "x": x,
            "y": y,
            "fontsize": fontsize,
            "fontfile": self.escape_arguments(self.get_fontfile(fontname)),
            "fontcolor": color + (f"@{alpha}" if alpha is not None else ""),
            "expansion": self.text_expansion_flag,
        }

        flags.update(kwargs)
        self.flags = flags

    def get_fontfile(self, fontname):
        if os.path.isabs(fontname) or "/" in fontname or "\\" in fontname:
            return fontname  # Already a full path

        if os.name == "nt":
            return f"C://Windows/Fonts/{fontname}"
        return f"/usr/share/fonts/truetype/freefont/{fontname}"
