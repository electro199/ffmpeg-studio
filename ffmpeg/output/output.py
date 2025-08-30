from typing import Iterable, Literal, Optional

from ..utils.commons import build_flags, wrap_quotes
from ..inputs import BaseInput, StreamSpecifier


class MetadataMixin:
    """
    Mixin to add metadata key=value pairs to an map/output.
    Stores metadata in a dict and expands to FFmpeg args on build.
    """

    def __init__(self):
        self._metadata: dict[str, str] = {}

    def add_metadata(self, key: str, value: str):
        """
        Add a metadata key=value pair.
        """
        self._metadata[key] = value

    def build_metadata(self, stream_spec: str = "") -> list[str]:
        """
        Expand stored metadata into FFmpeg args.
        """
        flags = []
        for key, value in self._metadata.items():
            if stream_spec:
                flags += ["-metadata" + stream_spec, f"{key}={wrap_quotes(value)}"]
            else:
                flags += ["-metadata", f"{key}={wrap_quotes(value)}"]
        return flags


# TODO stream_type can be inferred from input node
class Map(MetadataMixin):
    def __init__(
        self,
        node: BaseInput | StreamSpecifier,
        suffix_flags: Optional[dict] = None,
        stream_type: Optional[Literal["a", "v", "s", "d", "t", "V"]] = None,
        **flags,
    ) -> None:
        """
        Represents a single input stream mapping for an FFmpeg output.

        This class encapsulates an input source (`BaseInput` or `StreamSpecifier`) along with
        optional stream type and FFmpeg-specific flags that will be applied during the mapping.

        Args:
            node (BaseInput | StreamSpecifier): The input source to map (either a full input or a specific stream).
            suffix_flags (Optional[dict], optional): Additional flags to apply **after** the `-map` option.
            stream_type (Optional[Literal["a", "v", "s", "d", "t", "V"]], optional): A shortcut to specify audio ('a'), video ('v'), or subtitle ('s') streams.
            **flags: Additional key-value FFmpeg flags applied directly to the mapping.

        Example:
            ```python
            Map(VideoFile("in.mp4").video, stream_type="v", codec="libx264")
            ```
        """
        super().__init__()
        self.node = node
        self.stream_type = stream_type
        self.suffix_flags = {}
        if suffix_flags:
            self.suffix_flags = {**suffix_flags}
        self.flags = {**flags}

    def build(self, map_index) -> list[str]:

        flags = []
        # use stream type like foo:v
        stream_type_specfier = f":{self.stream_type}" if self.stream_type else ""

        for k, v in self.suffix_flags.items():
            flags.append(f"-{k}{stream_type_specfier}:{map_index}")
            flags.append(str(v))

        for k, v in self.flags.items():
            flags.append(f"-{k}")
            flags.append(str(v))

        flags.extend(self.build_metadata(stream_type_specfier))

        return flags


class OutFile(MetadataMixin):
    def __init__(
        self,
        maps: Iterable[Map],
        path,
        *,
        metadata: Optional[dict[str, str]] = None,
        **kvflags,
    ) -> None:
        """
        Represents an FFmpeg output configuration.

        This class wraps multiple mapped inputs (as `Map` objects), the output file path,
        and any output flags.

        Args:
            maps (Iterable[Map]): List of `Map` objects defining which input streams to include.
            path (str): Output file path (e.g., `"out.mp4"`).
            metadata (dict[str, str]): Metadata key-value pairs to add to the output file.
            **kvflags: Additional key-value FFmpeg output flags (e.g., `crf=23`, `preset="fast"`).

        Example:
            ```python
            OutFile(
                maps=[
                    Map(VideoFile("input.mp4").video),
                    Map(VideoFile("input.mp4").audio)
                ],
                path="output.mp4",
                crf=23,
                preset="fast",
                metadata={"title": "My Video", "author": "Me"}
            )
            ```
        """
        super().__init__()
        self.maps = maps
        self.path = path
        self.kvflags = kvflags
        self._metadata = metadata or {}

    def build(self) -> list[str]:
        """
        Build output flags.
        Includes metadata, flags and output path.
        """
        return [*build_flags(self.kvflags), *self.build_metadata(), self.path]
