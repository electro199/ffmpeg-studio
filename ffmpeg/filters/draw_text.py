import os
import re
from typing import Literal, Optional

from .base import BaseFilter
from .mixins.enable import TimelineEditingMixin


def escape_stray_percent(s: str) -> str:
    # Add a backslash before any '%' not followed by '{'
    return re.sub(r"%(?!\{)", r"\\\\%", s)


class Text(BaseFilter, TimelineEditingMixin):
    """
    Draw a text string or text from a specified file on top of a video,
    using the libfreetype library.
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
        text_expansion: bool = False,
        **kwargs,
    ):
        super().__init__("drawtext")

        flags = {
            "text": (
                escape_stray_percent(self.escape_arguments(text))
                if text_expansion
                else self.escape_arguments(text)
            ),
            "x": x,
            "y": y,
            "fontsize": fontsize,
            "fontfile": self.escape_arguments(self.get_fontfile(fontname)),
            "fontcolor": color + (f"@{alpha}" if alpha is not None else ""),
            "expansion": text_expansion,
        }

        flags.update(kwargs)
        self.flags = flags

    def get_fontfile(self, fontname):
        if os.path.isabs(fontname) or "/" in fontname or "\\" in fontname:
            return fontname  # Already a full path

        if os.name == "nt":
            return f"C://Windows/Fonts/{fontname}"
        return f"/usr/share/fonts/truetype/freefont/{fontname}"

    # text expansion escaping relies on
    # self.escape_arguments to escape `:` and `\`
    # by combination of both following code works

    @staticmethod
    def f_expression(expr) -> str:
        """
        Returns an FFmpeg drawtext expansion string
        that evaluate expression.
        """
        return f"%{{expr:{expr}}}"

    @staticmethod
    def f_gmtime(fmt: str = "%a %b %d %Y") -> str:
        """
        Returns an FFmpeg drawtext expansion string
        that expands to the local time with given strftime format.
        """
        fmt = fmt.replace(":", "\\:")
        return f"%{{gmtime:{fmt}}}"

    @staticmethod
    def f_localtime(fmt: str = "%a %b %d %Y") -> str:
        """
        Returns an FFmpeg drawtext expansion string
        that expands to the local time with given strftime format.
        """
        fmt = fmt.replace(":", "\\:")
        return f"%{{localtime:{fmt}}}"

    @staticmethod
    def f_frame_num() -> str:
        """
        Returns an FFmpeg drawtext expansion string
        that expands to the local time with given strftime format.
        """
        return "%{frame_num}"

    @staticmethod
    def f_pts(
        fmt: Literal["flt", "hms", "gmtime", "localtime"] = "flt",
        offset: Optional[str] = None,
        extra: Optional[str] = None,
    ) -> str:
        """
        Returns an FFmpeg drawtext expansion string
        that expands to the PTS (presentation timestamp).

        Args:
            fmt: Format of the timestamp.
                - "flt"       -> seconds with microsecond precision (default)
                - "hms"       -> [-]HH:MM:SS.mmm
                - "gmtime"    -> UTC timestamp (strftime supported if extra is given)
                - "localtime" -> local timestamp (strftime supported if extra is given)
            offset: Offset to add to timestamp (e.g., "10" for +10s).
            extra: Optional third argument:
                - for "hms" format: "24HH"
                - for gmtime/localtime: strftime format string.

        Examples:
            f_pts() -> "%{pts}"
            f_pts("hms") -> "%{pts:hms}"
            f_pts("hms", "5") -> "%{pts:hms:5}"
            f_pts("localtime", "0", "%H\\:%M\\:%S") -> "%{pts:localtime:0:%H\\:%M\\:%S}"
        """
        args = [fmt]
        if offset is not None:
            args.append(offset)
        if extra is not None:
            # escape colons in extra because ffmpeg uses ':' as separator
            extra = extra.replace(":", "\\:")
            args.append(extra)

        if args:
            return f"%{{pts:{':'.join(args)}}}"
        return "%{pts}"
