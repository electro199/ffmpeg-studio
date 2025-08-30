from typing import Literal, Optional

from .base import BaseFilter
from .mixins.enable import TimelineEditingMixin


class Volume(BaseFilter, TimelineEditingMixin):
    """
    Volume Adjust using FFmpeg's `volume` filter.
    """

    def __init__(
        self,
        value: str | float,
        precision: Optional[
            Literal[
                "fixed",
                "float",
                "double",
            ]
        ] = None,
        eval: Optional[
            Literal[
                "once",
                "frame",
            ]
        ] = None,
        replaygain: Optional[
            Literal[
                "drop",
                "ignore",
                "track",
                "album",
            ]
        ] = None,
        replaygain_noclip: Optional[int] = None,
        replaygain_preamp: Optional[bool] = None,
    ):
        super().__init__("volume")

        self.flags = {
            "volume": value,
            "precision": precision,
            "eval": eval,
            "replaygain": replaygain,
            "replaygain_noclip": replaygain_noclip,
            "replaygain_preamp": replaygain_preamp,
        }
