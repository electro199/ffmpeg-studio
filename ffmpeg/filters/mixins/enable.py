from typing import Self


class TimelineEditingMixin:
    """
    Mixin providing timeline-based activation control for FFmpeg filter graphs.

    This mixin allows enabling filters conditionally based on the video timestamp,
    using FFmpeg's `enable` expression mechanism with `between`, `gte`, and `lte`.

    Attributes:
        flags (dict): Dictionary storing FFmpeg filter options, such as enable expressions.
    """

    flags: dict

    def enable_between(self, start, end) -> Self:
        """
        Enable the filter only between the given start and end times.

        Args:
            start (float): Start time (in seconds).
            end (float): End time (in seconds).

        Returns:
            TimelineEditingMixin: The current instance with the updated `enable` flag.
        """
        self.flags.update({"enable": rf"between(t\,{start}\,{end})"})
        return self

    def enable_after(self, t: float) -> Self:
        """
        Enable the filter only after the given timestamp.

        Args:
            t (float): Time (in seconds) after which the filter is enabled.

        Returns:
            TimelineEditingMixin: The current instance with the updated `enable` flag.
        """
        self.flags.update({"enable": rf"gte(t\,{t})"})
        return self

    def enable_before(self, t: float) -> Self:
        """
        Enable the filter only before the given timestamp.

        Args:
            t (float): Time (in seconds) before which the filter is enabled.

        Returns:
            TimelineEditingMixin: The current instance with the updated `enable` flag.
        """
        self.flags.update({"enable": rf"lte(t\,{t})"})
        return self
