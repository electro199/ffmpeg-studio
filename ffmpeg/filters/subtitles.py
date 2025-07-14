from typing import Optional
from .base import BaseFilter


class Subtitles(BaseFilter):

    def __init__(
        self,
        filename: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        fontsdir: Optional[str] = None,
        alpha: Optional[bool] = None,
        charenc: Optional[str] = None,
        stream_index: Optional[int] = None,
        force_style: Optional[str] = None,
        wrap_unicode: Optional[bool] = None,
    ):
        """
        Draw subtitles on top of input video using the libass library.

        Args:
            filename (Optional[int]): Set the filename of the subtitle file to read. It must be specified.

            original_size (Optional[int]): Specify the size of the original video, the video for which the ASS file was composed. For the syntax of this option, check the (ffmpeg-utils)"Video size" section in the ffmpeg-utils manual. Due to a misdesign in ASS aspect ratio arithmetic, this is necessary to correctly scale the fonts if the aspect ratio has been changed.

            fontsdir (Optional[str]): Set a directory path containing fonts that can be used by the filter. These fonts will be used in addition to whatever the font provider uses.

            alpha (Optional[bool]): Process alpha channel, by default alpha channel is untouched.

            charenc (Optional[str]): Set subtitles input character encoding. subtitles filter only. Only useful if not UTF-8.

            stream_index, si (Optional[int]): Set subtitles stream index. subtitles filter only.

            force_style (Optional[str]): Override default style or script info parameters of the subtitles. It accepts a string containing ASS style format KEY=VALUE couples separated by ",".

            wrap_unicode (Optional[bool]): Break lines according to the Unicode Line Breaking Algorithm. Availability requires at least libass release 0.17.0 (or LIBASS_VERSION 0x01600010), and libass must have been built with libunibreak.

        The option is enabled by default except for native ASS.
        """
        super().__init__("subtitles")

        original_size = None
        if width and height:
            original_size = f"{width}x{height}"

        self.flags = {
            "filename": self.escape_arguments(filename),
            "original_size": original_size,
            "fontsdir": self.escape_arguments(fontsdir),
            "alpha": alpha,
            "charenc": charenc,
            "stream_index": stream_index,
            "force_style": self.escape_arguments(force_style),
            "wrap_unicode": wrap_unicode,
        }
