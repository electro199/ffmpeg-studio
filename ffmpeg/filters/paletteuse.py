from typing import Literal

from .base import BaseFilter
from ..inputs import BaseInput, StreamSpecifier


class PaletteUse(BaseFilter):

    def __init__(
        self,
        palette: BaseInput | StreamSpecifier,
        dither: (
            Literal[
                "bayer",
                "heckbert",
                "floyd_steinberg",
                "sierra2",
                "sierra2_4a",
                "sierra3",
                "burkes",
                "atkinson",
            ]
            | None
        ) = None,
        bayer_scale: int | None = None,
        diff_mode: bool | None = None,
        new: bool | None = None,
        alpha_threshold: int | None = None,
        debug_kdtree: str | None = None,
    ):
        """
        Find the optimal palette for a given stream.
        """
        super().__init__("paletteuse")

        self.palette = palette

        if alpha_threshold is not None and (
            alpha_threshold > 255 or alpha_threshold < 0
        ):
            raise ValueError(
                f"alpha_threshold must be from 0 to 255. provided={alpha_threshold}"
            )

        if diff_mode is not None and (diff_mode > 5 or diff_mode < 0):
            raise ValueError(f"diff_mode must be from 0 to 5. provided={diff_mode}")

        self.flags = {
            "dither": dither,
            "bayer_scale": bayer_scale,
            "diff_mode": diff_mode,
            "new": new,
            "alpha_threshold": alpha_threshold,
            "debug_kdtree": self.escape_arguments(debug_kdtree),
        }

    def _register_parent(self, *background: BaseInput | StreamSpecifier):
        # Expecting two inputs by default (background and overlay)
        self._check_register()
        if len(background) > 1:
            raise ValueError("Overlay filter expects only one background input")

        self.parent_nodes.extend(background)
        self.parent_nodes.append(self.palette)
