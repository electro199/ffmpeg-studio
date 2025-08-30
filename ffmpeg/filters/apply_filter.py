"""
Apply FFmpeg filters to input streams or output from another filter.

Use `apply` when filter outputs single output like Overlay, Text or Scale
Use `apply2` when filter outputs multiple outputs like Split or Concat

Internally  it add input in parent list attr and return the output it helps filter to be flexible
"""

from .base import BaseFilter
from ..inputs import BaseInput, StreamSpecifier


def apply(
    node: BaseFilter,
    *parent: BaseInput | StreamSpecifier,
) -> StreamSpecifier:
    """
    Apply a filter input streams.

    This function connects the given input nodes (either BaseInput or StreamSpecifier)
    to a filter node and returns a single output stream from the filter.

    Args:
        node (BaseFilter): The filter node to apply.
        *parent (BaseInput | StreamSpecifier): Input nodes to connect to the filter.

    Returns:
        StreamSpecifier: The resulting single output stream from the filter.
    """
    node.parent_nodes.extend(parent)
    return node.get_outputs()  # type: ignore


def apply2(
    node: BaseFilter,
    *parent: BaseInput | StreamSpecifier,
) -> list[StreamSpecifier]:
    """
    Apply a filter input streams.

    This function connects the given input nodes (either BaseInput or StreamSpecifier)
    to a filter node and returns a list of all output streams from the filter.

    Args:
        node (BaseFilter): The filter node to apply.
        *parent (BaseInput | StreamSpecifier): Input nodes to connect to the filter.

    Returns:
        list[StreamSpecifier]: A list of output streams from the filter.
    """
    node.parent_nodes.extend(parent)
    return node.get_outputs()  # type: ignore
