from typing import Literal

from .base import BaseFilter


class FPS(BaseFilter):

    def __init__(
        self,
        fps: float | str,
        start_time: int | None = None,
        round: (
            Literal[
                "zero",
                "inf",
                "down",
                "up",
                "near",
            ]
            | None
        ) = None,
        eof_action: Literal["round", "pass"] | None = None,
    ):
        """
        Convert the video to specified constant frame rate
        by duplicating or dropping frames as necessary.
        """
        super().__init__("fps")

        self.flags = {
            "fps": fps,
            "start_time": start_time,
            "round": round,
            "eof_action": eof_action,
        }
