from typing import Any, Optional

from .base_virtual_input import BaseVirtualInput


class VirtualAudio(BaseVirtualInput):
    """Generate audio with ffmpeg"""

    def __init__(
        self,
        name: str,
        format: str = "lavfi",
        flags: Optional[dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        super().__init__(name=name, format=format, flags=flags, size=None, **kwargs)

    @classmethod
    def from_noise(
        cls,
        color: str = "white",
        amplitude: float = 1.0,
        duration: Optional[float] = None,
        sample_rate: int = 44100,
    ):
        """
        Generate noise audio (white, pink, brown).

        https://ffmpeg.org/ffmpeg-filters.html#anoisesrc
        """
        kwargs = dict(
            color=color,
            amplitude=amplitude,
            r=sample_rate,
        )
        if duration is not None:
            kwargs["d"] = duration

        return cls("anoisesrc", **kwargs)

    @classmethod
    def from_expression(
        cls,
        expr: str,
        duration: Optional[float] = None,
        sample_rate=None,
        channels=None,
    ):
        """
        Generate audio from mathematical expression.

        Example: abs(mod(n*0.01,2)-1) => bouncing wave
        https://ffmpeg.org/ffmpeg-filters.html#aevalsrc
        """
        kwargs = dict(
            exprs=(expr),
            s=sample_rate,
            c=channels,
        )
        if duration is not None:
            kwargs["d"] = duration

        return cls("aevalsrc", **kwargs)
