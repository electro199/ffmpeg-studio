from typing import Optional, Self
from .streams import StreamSpecifier
from abc import ABC, abstractmethod
from ..utils.commons import build_flags


class BaseInput(ABC):
    def __init__(self, stream_type: Optional[str] = None, **kwargs) -> None:
        self.flags = kwargs
        self.stream_type = stream_type

    def set_flag(self, key: str, value: Optional[str] = None) -> Self:
        self.flags.update({key: value})
        return self

    @abstractmethod
    def _build_input_flags(self) -> list[str]:
        raise NotImplementedError()

    def _build(self):
        return build_flags(self.flags)

    def _get_outputs(self):
        return StreamSpecifier(self)
