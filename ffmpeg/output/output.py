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

    def _build_metadata(self, stream_spec: str = "") -> list[str]:
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


class Map(MetadataMixin):
    def __init__(
        self,
        node: BaseInput | StreamSpecifier,
        suffix_flags: Optional[dict] = None,
        stream_type: Optional[Literal["a", "v", "s", "d", "t", "V"]] = None,
        metadata: Optional[dict[str, str]] = None,
        **flags,
    ) -> None:
        """
        Represents a mapping of an input stream to an output.
        This class wraps an input node (like a file or filter), optional flags, and metadata.

        Args:
            node: The input node or stream specifier to map from.
            suffix_flags: Flags that apply specifically to this map, like `-c:v`.
            stream_type: Stream type specifier ('a', 'v', 's', 'd', 't', 'V').
            metadata: Metadata key-value pairs to add to this mapped stream.
            **flags: Additional key-value FFmpeg flags for this map (e.g., `disposition=default`).
        """
        super().__init__()
        self.node = node
        # If node is a StreamSpecifier, use its stream_type if not provided
        self.stream_type = stream_type or (
            getattr(node, "stream_type", None) if isinstance(node, BaseInput) else None
        )
        self.suffix_flags = dict(suffix_flags) if suffix_flags else {}
        self.flags = dict(flags)
        self._metadata = metadata or {}

    def _build(self, stream: str, map_index: int) -> list[str]:

        # use stream type like foo:v
        stream_type_specfier = f":{self.stream_type}" if self.stream_type else ""

        flags: list[str] = [f"-map{stream_type_specfier}", stream]

        for k, v in self.suffix_flags.items():
            flags.append(f"-{k}{stream_type_specfier}:{map_index}")
            flags.append(str(v))

        for k, v in self.flags.items():
            flags.append(f"-{k}")
            flags.append(str(v))

        flags.extend(self._build_metadata(f":s{stream_type_specfier}:{map_index}"))

        return flags


class OutFile(MetadataMixin):
    def __init__(
        self,
        maps: Iterable[Map],
        path: str,
        *,
        metadata: Optional[dict[str, str]] = None,
        **kvflags,
    ) -> None:
        """
        Represents an FFmpeg output configuration.

        This class wraps multiple mapped inputs (as `Map` objects), the output file path,
        and any output flags.

        Args:
            maps: List of `Map` objects defining which input streams to include.
            path: Output file path (e.g., `"out.mp4"`).
            metadata : Metadata key-value pairs to add to the output file.
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

    def _build(self) -> list[str]:
        """
        Build output flags.
        Includes metadata, flags and output path.
        """
        return [*build_flags(self.kvflags), *self._build_metadata(), self.path]
