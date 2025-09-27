from typing import Literal, Optional

from ..utils.commons import build_flags
from .base_input import BaseInput
from .options.file_input_option import FileInputOptions
from .streams import StreamSpecifier


class InputFile(BaseInput):
    """
    General Input for FFMPEG backend You can use custom flags
    """

    def __init__(
        self, filepath: str, options: Optional[FileInputOptions] = None, **kwargs
    ) -> None:
        super().__init__(**kwargs)  # No specific stream type for general input
        self.filepath = filepath
        self.options = options

    def _build_input_flags(self) -> list[str]:
        command = []
        if self.options:
            command.extend(self.options.build())
        command.extend([*build_flags(self.flags), "-i", self.filepath])
        return command

    def __repr__(self) -> str:
        return f"<InputFile {self.filepath}>"

    @property
    def audio(self):
        return StreamSpecifier(self, stream_name="a")

    @property
    def video(self):
        return StreamSpecifier(self, stream_name="v")

    def get_stream(
        self,
        stream_index: int,
        stream_name: Optional[Literal["a", "v", "s", "d", "t", "V"]] = None,
    ) -> StreamSpecifier:
        return StreamSpecifier(self, stream_name=stream_name, stream_index=stream_index)
