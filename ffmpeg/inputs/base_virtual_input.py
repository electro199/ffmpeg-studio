from typing import Any, Optional

from ..utils import build_flags, build_name_kvargs_format
from .file_input import BaseInput


class BaseVirtualInput(BaseInput):
    def __init__(
        self,
        name: str,
        format: str = "lavfi",
        flags: Optional[dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**flags or {})
        self.name = name
        self.format_flag = format
        self.kwargs = kwargs

        # Size is required to make support the get_size function
        # most filters support size for output size otherwise
        # _size can be used to pass the size
        if not (s := kwargs.get("_size")):
            s = kwargs["size"]
        else:
            kwargs.pop("_size")
        self.__size: str = s

    def _build_input_flags(self) -> list[str]:
        """
        Builds the FFmpeg input flags for the video file.

        This method constructs the FFmpeg command line input flags to specify
        the video file to be processed.

        Returns:
            list[str]: A list of input flags for FFmpeg, including the file path.
        """
        f = build_flags(self.flags)
        f.extend(
            ["-f", "lavfi", "-i", build_name_kvargs_format(self.name, self.kwargs)]
        )
        return f

    def get_size(self) -> tuple[int, int]:
        """
        Retrieves the resolution (width and height).

        Returns:
            tuple[int, int]: A tuple containing the width and height of the video.
        """
        w, h = self.__size.split("x")
        return int(w), int(h)

    def _build(self) -> list:
        return ["-f", self.format_flag, "-i", self.input_flag]

    # ---------------------- VIDEO SOURCES ----------------------

    # ---------------------- AUDIO SOURCES ----------------------

    @classmethod
    def aevalsrc(cls, exprs: str = "sin(2*PI*440*t)", duration: float = None):
        kwargs = {"exprs": exprs}
        if duration:
            kwargs["duration"] = duration
        return cls("aevalsrc", **kwargs)

    # ---------------------- AUDIO FILTER VISUALS ----------------------

    @classmethod
    def showwaves(cls, duration: int = 5):
        return cls("sine", frequency=440, duration=duration)  # Add showwaves filter

    @classmethod
    def showspectrum(cls, duration: int = 5):
        return cls("sine", frequency=440, duration=duration)  # Add showspectrum filter

    @classmethod
    def avectorscope(cls, duration: int = 5):
        return cls("sine", frequency=440, duration=duration)  # Add avectorscope

    @classmethod
    def showcqt(cls, duration: int = 5):
        return cls("sine", frequency=440, duration=duration)  # Add showcqt

    @classmethod
    def showspectrumpic(cls, duration: int = 5):
        return cls("sine", frequency=440, duration=duration)  # Add showspectrumpic

    @classmethod
    def showcwt(cls, duration: int = 5):
        return cls("sine", frequency=440, duration=duration)  # Add showcwt
