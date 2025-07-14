import os
from typing import Optional
from .base import BaseFilter
from .mixins.enable import TimelineEditingMixin


class Text(BaseFilter, TimelineEditingMixin):
    """
    Draw text using `drawtext` filter
    """

    def __init__(
        self, text, y, x, fontsize=16, color="white", fontname="arial.ttf", **kwargs
    ):
        super().__init__("drawtext")
        self.flags = {
            "text": self.escape_arguments(text),
            "fontfile": self.escape_arguments(self.get_fontfile(fontname)),
            "fontsize": fontsize,
            "x": x,
            "y": y,
            "fontcolor": color,
        }
        self.flags.update(kwargs)

    def get_fontfile(self, fontname):
        return (
            "C://Windows/Fonts/" + fontname
            if os.name == "nt"
            else "/usr/share/fonts/truetype/freefont/" + fontname
        )

    # FIXME get correct escaping
    # @classmethod
    # def f_gmtime(cls, strftime: Optional[str] = None) -> str:
    #     """
    #     Build FFmpeg drawtext expression to show UTC (GMT) time during video rendering.

    #     Args:
    #         strftime: Optional strftime format string (e.g. "%Y-%m-%d %H:%M:%S")
    #     """
    #     e = "gmtime"
    #     if strftime:
    #         e += (f":{((cls.escape_arguments(strftime)))}").replace("\\", "\\\\").replace(":", "\\\\:")
    #     return "%{" + e + "}"

    # @classmethod
    # def f_localtime(cls, strftime: Optional[str] = None) -> str:
    #     """
    #     Build FFmpeg drawtext expression to show local system time during rendering.

    #     Args:
    #         strftime: Optional strftime format string (e.g. "%H:%M:%S")
    #     """
    #     e = "localtime"
    #     if strftime:
    #         e += (f"\\:{cls.escape_arguments(strftime)}")
    #     return "%{" + e + "}"

    # @classmethod
    # def f_pts(
    #     cls, fmt: str = "hms", offset: Optional[str] = None, third: Optional[str] = None
    # ) -> str:
    #     """
    #     Build FFmpeg drawtext expression to show presentation timestamp (PTS) of each frame.

    #     Args:
    #         fmt: Format type — 'flt' (default, seconds), 'hms' (HH:MM:SS), 'gmtime', or 'localtime'
    #         offset: Optional offset to add to the time (e.g. "5.0" for 5s shift)
    #         third: Optional 3rd argument (e.g. a strftime format if fmt is 'localtime' or 'gmtime')
    #     """
    #     e = f"pts:{fmt}"
    #     if offset:
    #         e += (f"\\\\:{cls.escape_arguments(offset)}")
    #     if third:
    #         e += (f"\\\\:{cls.escape_arguments(third)}")
    #     return "%{" + e + "}"

    # @classmethod
    # def f_expr(cls, expr: str) -> str:
    #     """
    #     Build FFmpeg drawtext expression to evaluate a custom mathematical expression.

    #     Args:
    #         expr: The expression to evaluate (e.g. "n/30" to show seconds at 30 fps)
    #     """
    #     e = "expr" + (f"\\\\:{cls.escape_arguments(expr)}")
    #     return "%{" + e + "}"

    # @classmethod
    # def f_metadata(cls, key: str, default: Optional[str] = None) -> str:
    #     """
    #     Build FFmpeg drawtext expression to read a metadata value from the input stream.

    #     Args:
    #         key: Metadata key to read (e.g. "lavfi.scene_score")
    #         default: Optional default value if metadata key is not found
    #     """
    #     e = "metadata" + cls.escape_arguments(f"\\\\:{cls.escape_arguments(key)}")
    #     if default:
    #         e += (f"\\\\:{cls.escape_arguments(default)}")
    #     return "%{" + e + "}"

    # @staticmethod
    # def f_frame() -> str:
    #     """
    #     Return FFmpeg drawtext expression for current frame number.
    #     """
    #     return "%{n}"
