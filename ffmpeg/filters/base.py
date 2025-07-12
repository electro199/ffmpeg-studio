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

from typing import Optional, TypeVar, Union
from ..inputs.streams import StreamSpecifier
from ..inputs.base_input import BaseInput
from ..utils import build_name_kvargs_format


OptionalStr = TypeVar("OptionalStr", None, str, Optional[str])
"""
String or None Type
"""


class BaseFilter:
    """Base class for all FFmpeg filters."""

    def __init__(self, filter_name: str) -> None:

        self.filter_name = filter_name
        self.flags: dict = {}  # all args

        self.parent_nodes: list[BaseInput | StreamSpecifier] = []
        self.parent_stream: list[int | str | None] = []

        self.output_count = 1

    def add_input(self, node: Union[BaseInput, StreamSpecifier]):
        self.parent_nodes.append(node)

    def build(self) -> str:
        return build_name_kvargs_format(self.filter_name, self.flags)

    def get_outputs(self):
        return (
            StreamSpecifier(self)
            if self.output_count == 1
            else [StreamSpecifier(self, i) for i in range(self.output_count)]
        )

    def escape_arguments(self, text: OptionalStr) -> OptionalStr:
        """
        Escapes all characters that require escaping in FFmpeg filter arguments.

        Returns:
            None if text was None otherwise new str with escaped chars
        """
        if text is None:
            return text
        return (
            "'"
            + text.replace("\\", "\\\\")
            .replace("'", r"'\\\''")
            .replace("%", r"\\%")
            .replace(":", "\\:")
            + "'"
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}, flags={self.flags}>"  # TODO get better printing scheme
