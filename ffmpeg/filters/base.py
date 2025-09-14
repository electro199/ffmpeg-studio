"""
Base For All Filters

Command structure represented are like this:

-i 1.png

-f_c    [1]filter=2=d:s:d[a] ;
        [a]filter=2=d:s:d[b]
        |----Filter-----|

Whole node in command
----
-f_c    [1]filter=2=d:s:d[a]
        [a]filter=2=d:s:d[b]
        |----Filter-----|
                        |*|
                        StreamSpecifier

Filter holds :
    parent node reference either (StreamSpecifier or Input)
    Filter Info including name and flags

"""

from typing import Any, Union

from ..inputs.base_input import BaseInput
from ..inputs.streams import StreamSpecifier
from ..utils import build_name_kvargs_format


class BaseFilter:
    """Base class for all FFmpeg filters."""

    def __init__(self, filter_name: str) -> None:

        self.filter_name = filter_name
        self.flags: dict = {}  # all args

        self.parent_nodes: list[BaseInput | StreamSpecifier] = []

        self.registered_parents = False
        self.output_count = 1

    def _register_parent(self, *node: Union[BaseInput, StreamSpecifier]):
        """Register parent nodes only once."""
        self._check_register()
        self.parent_nodes.extend(node)

    def _check_register(self):
        if self.registered_parents:
            raise RuntimeError(
                "Parent nodes can only be registered once, Please make new filter instance"
            )
        self.registered_parents = True

    def _build(self) -> str:
        return build_name_kvargs_format(self.filter_name, self.flags)

    def _get_outputs(self):
        return (
            StreamSpecifier(self)
            if self.output_count == 1
            else [StreamSpecifier(self, i) for i in range(self.output_count)]
        )

    def escape_arguments(self, text: Any) -> Any | str:
        """
        Escapes all characters that require escaping in FFmpeg filter arguments.

        Returns:
            None if text was None otherwise new str with escaped chars
        """
        if not isinstance(text, str):
            return text
        return (
            "'"
            + text.replace("\\", "\\\\").replace("'", r"'\\\''").replace(":", "\\:")
            + "'"
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}, flags={self.flags}>"  # TODO get better printing scheme
