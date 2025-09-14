from typing import Literal, Optional

from ffmpeg.inputs.base_input import BaseInput

from ..inputs import BaseInput, StreamSpecifier
from .base import BaseFilter


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
        self.parent_nodes = [*nodes]
        self.flags["duration"] = end_on
        self.flags["normalize"] = normalize
        self.flags["weights"] = " ".join(map(str, weights)) if weights else None
        self.flags["dropout_transition"] = dropout_transition

    def _register_parent(self, *node: BaseInput | StreamSpecifier):
        self._check_register()
        self.parent_nodes.extend(node)
        self.flags["inputs"] = len(self.parent_nodes)

    def _get_outputs(self):
        return [StreamSpecifier(self, i) for i in range(self.output_count)]
