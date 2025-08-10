from typing import Literal, Optional
from .base import BaseFilter
from ..inputs.streams import StreamSpecifier


class AudioMix(BaseFilter):
    """
    AudioMix using FFmpeg's `amix` filter.
    """

    def __init__(
        self,
        *nodes,
        end_on: Optional[
            Literal[
                "longest",
                "shortest",
                "first",
            ]
        ] = None,
        normalize: Optional[bool] = None,
        dropout_transition: Optional[float] = None,
        weights: Optional[list[float]] = None,
    ):
        super().__init__("amix")
        self.clips = nodes
        self.parent_nodes = []
        self.flags["inputs"] = (
            len(self.clips) + 1
        )  # assuming the first one is from apply function
        self.flags["duration"] = end_on
        self.flags["normalize"] = normalize
        self.flags["weights"] = " ".join(map(str, weights)) if weights else None
        self.flags["dropout_transition"] = dropout_transition

    def get_outputs(self):
        if self.clips != self.parent_nodes:
            self.parent_nodes.extend(self.clips)

        return (
            StreamSpecifier(self)
            if self.output_count == 1
            else [StreamSpecifier(self, i) for i in range(self.output_count)]
        )
