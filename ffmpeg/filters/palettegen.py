from typing import Literal

from .base import BaseFilter


class PaletteGen(BaseFilter):

    def __init__(
        self,
        max_colors: int | None = None,
        reserve_transparent: bool | None = None,
        stats_mode: (
            Literal[
                "full",
                "diff",
                "single",
            ]
            | None
        ) = None,
    ):
        """
        Find the optimal palette for a given stream.
        """
        super().__init__("palettegen")

        if max_colors is not None and (max_colors > 256 or max_colors < 2):
            raise ValueError(f"max_colors must be from 2 to 256. provided={max_colors}")

        self.flags = {
            "max_colors": max_colors,
            "reserve_transparent": reserve_transparent,
            "stats_mode": stats_mode,
        }
