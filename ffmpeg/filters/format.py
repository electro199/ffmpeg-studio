from typing import Optional
from .base import BaseFilter


class Format(BaseFilter):
    """
    Represents a format filter that sets the pixel format of a video stream.
    """

    def __init__(
        self,
        pixel_format: str,
        color_space: Optional[str] = None,
        color_range: Optional[str] = None,
        alpha_mode: Optional[str] = None,
    ):
        """
        Convert the input video to one of the specified pixel formats. Libavfilter will try to pick one that is suitable as input to the next filter.

        It accepts the following parameters:

        Arguments:
            pixel_format:
                A `|`-separated list of pixel format names, such as "pix_fmts=yuv420p|monow|rgb24".

            color_space:
                A `|`-separated list of color space names, such as "color_spaces=bt709|bt470bg|bt2020nc".

            color_range:
                A `|`-separated list of color range names, such as "color_ranges=tv|pc".

            alpha_mode:
                A `|`-separated list of color range names, such as "alpha_modes=straight|premultiplied".
        """
        super().__init__("format")
        self.flags["pix_fmts"] = pixel_format
        self.flags["color_spaces"] = color_space
        self.flags["color_ranges"] = color_range
        self.flags["alpha_modes"] = alpha_mode
