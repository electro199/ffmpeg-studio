from ..inputs import BaseInput, StreamSpecifier
from ..inputs.streams import StreamSpecifier
from .base import BaseFilter
from .mixins.enable import TimelineEditingMixin


class Overlay(BaseFilter, TimelineEditingMixin):
    """
    Represents an overlay filter that combines two video streams.

    """

    def __init__(
        self,
        overlay_input: BaseInput | StreamSpecifier,
        x: str | float,
        y: str | float,
        **kwargs,
    ):

        super().__init__("overlay")
        self.overlay_node = overlay_input
        self.flags.update(kwargs)
        self.flags["x"] = self.escape_arguments(x)
        self.flags["y"] = self.escape_arguments(y)

    def _register_parent(self, *background: BaseInput | StreamSpecifier):
        # Expecting two inputs by default (background and overlay)
        self._check_register()
        if len(background) > 1:
            raise ValueError("Overlay filter expects only one background input")

        self.parent_nodes.extend(background)
        self.parent_nodes.append(self.overlay_node)
