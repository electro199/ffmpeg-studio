from typing import Literal, Optional


class StreamSpecifier:
    """
    Used specify in ffmpeg command

    ffmpeg docs : https://ffmpeg.org/ffmpeg.html#toc-Automatic-stream-selection
    """

    __slots__ = (
        "parent",
        "stream_index",
        "stream_name",
        "output_number",
        "codec_type",
        "metadata",
    )

    def __init__(
        self,
        parent,
        output_index=0,
        stream_index: Optional[int] = None,
        stream_name: Optional[Literal["a", "v", "s", "d", "t", "V"]] = None,
        codec_type: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> None:
        self.parent = parent
        self.stream_index = stream_index
        self.stream_name = stream_name
        self.output_number = output_index
        self.codec_type = codec_type
        self.metadata = metadata

    def build_stream_str(self):
        s = ""
        if self.stream_name:
            s += ":" + str(self.stream_name)

        if self.stream_index is not None:
            s += ":" + str(self.stream_index)

        return s

    def get_outputs(self):
        return StreamSpecifier(self)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} stream_index={self.stream_index} stream_name={self.stream_name}>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} index={self.stream_index} stream={self.stream_name}>"
