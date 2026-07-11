from ffmpeg.inputs.base_input import BaseInput
from .base import BaseFilter
from ..inputs.streams import StreamSpecifier
from ..inputs import BaseInput, StreamSpecifier


class VerticalStack(BaseFilter):
    """
    Represents an vstack filter that combines streams.

    Usage:
        ```
        vstack = VerticalStack(input1, input2, end_on_shortest=True)
        apply(vstack, input3, input4)
        ```
    """

    def __init__(self, *nodes: BaseInput, end_on_shortest: bool = False):
        super().__init__("vstack")

        self.parent_nodes = [*nodes]
        self.flags["shortest"] = int(end_on_shortest)

    def _register_parent(self, *node: BaseInput | StreamSpecifier):
        self._check_register()
        self.parent_nodes.extend(node)
        self.flags["inputs"] = len(self.parent_nodes)
