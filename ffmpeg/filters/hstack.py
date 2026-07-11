from ..inputs import BaseInput, StreamSpecifier
from .base import BaseFilter


class HorizontalStack(BaseFilter):
    """
    Represents an hstack filter that combines streams.

    """

    def __init__(
        self, *nodes: BaseInput | StreamSpecifier, end_on_shortest: bool = False
    ):
        super().__init__("hstack")
        self.parent_nodes = [*nodes]
        self.flags["shortest"] = int(end_on_shortest)

    def _register_parent(self, *node: BaseInput | StreamSpecifier):
        self._check_register()
        self.parent_nodes.extend(node)
        self.flags["inputs"] = len(self.parent_nodes)
