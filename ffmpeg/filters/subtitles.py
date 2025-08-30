from typing import Optional
from .base import BaseFilter


class Subtitles(BaseFilter):
    """
    Draw subtitles on top of input video using the libass library.
    """

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
