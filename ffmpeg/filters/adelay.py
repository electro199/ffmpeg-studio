from typing import Optional

from .base import BaseFilter
from .mixins.enable import TimelineEditingMixin


class AudioDelay(BaseFilter, TimelineEditingMixin):
    """
    Add Delay in Audio using FFmpeg's `adelay` filter.
    """

    def __init__(
        self,
        delay: list[float],
        all_channels: Optional[bool] = None,
    ):
        super().__init__("adelay")

        self.flags = {
            "delays": "|".join(
                map(str, delay),
            ),
            "all_channels": all_channels,
        }
