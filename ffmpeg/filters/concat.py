from typing import Optional, Union

from ffmpeg.inputs.base_input import BaseInput

from ..inputs import BaseInput, StreamSpecifier
from ..inputs.streams import StreamSpecifier
from .base import BaseFilter


class Concat(BaseFilter):
    """
    Represents a concat filter that joins multiple segments.
    See: https://ffmpeg.org/ffmpeg-filters.html#concat
    """

    def __init__(
        self,
        *nodes: BaseInput | StreamSpecifier,
        n: Optional[int],
        v: Optional[int] = 1,
        a: Optional[int] = 0,
        unsafe: bool = False,
    ):
        super().__init__("concat")
        self.parent_nodes = list(nodes)
        self.flags = {"n": n, "v": v, "a": a, "unsafe": unsafe}

    def _get_outputs(self):
        self.output_count = self.flags["v"] + self.flags["a"]
        return [StreamSpecifier(self, i) for i in range(self.output_count)]
