"""
Apply FFmpeg filters to input streams or output from another filter.

Use `apply` when filter outputs single output like Overlay, Text or Scale
Use `apply2` when filter outputs multiple outputs like Split or Concat

Internally  it add input in parent list attr and return the output it helps filter to be flexible
"""

from .base import BaseFilter
from ..inputs import BaseInput, StreamSpecifier


def apply(
    filter_obj: BaseFilter,
    *parent: BaseInput | StreamSpecifier,
) -> StreamSpecifier:
    """
    Apply a filter input streams.

    This function connects the given input nodes (either BaseInput or StreamSpecifier)
    to a filter node and returns a single output stream from the filter.

    Args:
        filter_obj: The filter node to apply.
        *parent: Input nodes to connect to the filter.

    Returns:
        The resulting single output stream from the filter.
    """
    if filter_obj.output_count > 1:
        raise ValueError(
            "Filter has multiple outputs, use apply2 function instead of apply"
        )
    filter_obj._register_parent(*parent)
    return filter_obj._get_outputs()  # type: ignore


def apply2(
    filter_obj: BaseFilter,
    *parent: BaseInput | StreamSpecifier,
) -> list[StreamSpecifier]:
    """
    Apply a filter input streams.

    This function connects the given input nodes (either BaseInput or StreamSpecifier)
    to a filter node and returns a list of all output streams from the filter.

    Args:
        filter_obj: The filter node to apply.
        *parent: Input nodes to connect to the filter.

    Returns:
        A list of output streams from the filter.
    """
    if filter_obj.output_count < 2:
        raise ValueError("Filter has single output, use apply function instead of apply2")
    
    filter_obj._register_parent(*parent)
    return filter_obj._get_outputs()  # type: ignore
