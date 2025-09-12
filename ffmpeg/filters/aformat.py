from typing import Optional
from .base import BaseFilter


class AudioFormat(BaseFilter):
    def __init__(
        self,
        sample_rates: Optional[list[str | float]] = None,
        sample_fmts: Optional[list[str | float]] = None,
        channel_layouts: Optional[list[str | float]] = None,
    ):
        """
        Represents an audio format filter that sets audio parameters.
        At least one of sample_rates, sample_fmts, or channel_layouts must be provided.

        Args:
            sample_rates: Optional list of sample rates (e.g., ["44100", "48000"]).
            sample_fmts: Optional list of sample formats (e.g., ["fltp", "s16"]).
            channel_layouts: Optional list of channel layouts (e.g., ["stereo", "5.1"]).
        """
        super().__init__("aformat")
        if not sample_rates and not sample_fmts and not channel_layouts:
            raise ValueError(
                "At least one of sample_rates, sample_fmts, or channel_layouts must be provided."
            )
        if sample_rates:
            self.flags["sample_rates"] = "|".join(map(str, sample_rates))

        if sample_fmts:
            self.flags["sample_fmts"] = "|".join(map(str, sample_fmts))

        if channel_layouts:
            self.flags["channel_layouts"] = "|".join(map(str, channel_layouts))
