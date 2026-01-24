from typing import Iterator, Literal, Optional
from .base_input import BaseInput
from .streams import StreamSpecifier
from ..ffprobe.ffprobe import ffprobe


class VideoFile(BaseInput):
    """
    A class representing a video file that can be processed with FFmpeg.

    This class provides methods for interacting with a video file, such as
    building FFmpeg input flags, extracting streams (audio, video, subtitles),
    creating subclips, and retrieving the video file's resolution.
    """

    def __init__(self, filepath: str, **kwargs) -> None:
        """
        Initializes the VideoFile object with the specified file path.

        Args:
            filepath: The path to the video file to be processed.
        """
        super().__init__(stream_type="v", **kwargs)
        self.filepath = filepath

    @property
    def audio(self) -> StreamSpecifier:
        """
        Access the audio stream of the video file.
        """
        return StreamSpecifier(self, stream_name="a")

    @property
    def video(self) -> StreamSpecifier:
        """
        Access the video stream of the video file.
        """
        return StreamSpecifier(self, stream_name="v")

    @property
    def subtitle(self) -> StreamSpecifier:
        """
        Access the subtitle stream of the video file.

        Returns:
            A StreamSpecifier object for the subtitle stream.
        """
        return StreamSpecifier(self, stream_name="s")

    def __iter__(self) -> Iterator[StreamSpecifier]:
        for stream in ffprobe(self.filepath)["streams"]:
            yield StreamSpecifier(
                self,
                stream_index=stream.get("index"),
                codec_type=stream.get("codec_type"),
                metadata=stream,
            )

    def __getitem__(self, index: int) -> StreamSpecifier:
        """
        Get stream from video by index
        """
        stream = ffprobe(self.filepath, ["-show_streams"])["streams"][index]
        return StreamSpecifier(
            self,
            stream_index=stream.get("index"),
            codec_type=stream.get("codec_type"),
            metadata=stream,
        )

    def get_stream(
        self,
        stream_index: int,
        stream_name: Optional[Literal["a", "v", "s", "d", "t", "V"]] = None,
    ) -> StreamSpecifier:
        """
        Get a specific stream from the video file by index and/or stream name.

        Note:
            This function will not validate if stream exists.

        Example:
            You get 2nd audio stream from video like this.
            ```python
            clip.get_stream(stream_index=1, stream_name="a")
            ```

        Args:
            stream_index: The index of the stream (e.g., 0 for the first stream).
            stream_name: The name of the stream
                to retrieve
                - `a` -> audio
                - `v` -> video
                - `s` -> subtitles
                - `d` -> data
                - `t` -> attachments
                - `V` -> video but excludes thumbnails/attached pics
                If not provided, retrieves the stream by index.

        Returns:
            A StreamSpecifier object for the requested stream.
        """
        return StreamSpecifier(self, stream_name=stream_name, stream_index=stream_index)

    def _build_input_flags(self) -> list[str]:
        """
        Builds the FFmpeg input flags for the video file.

        This method constructs the FFmpeg command line input flags to specify
        the video file to be processed.

        Returns:
            A list of input flags for FFmpeg, including the file path.
        """
        command = self._build()
        command.extend(["-i", self.filepath])
        return command

    def subclip(self, start: float | str, duration: float | str) -> "VideoFile":
        """
        Defines a subclip from the video file by setting the start and duration.
        This will not make a new copy until exported.

        Args:
            start: The start time of the subclip.
            duration: The duration of the subclip.

        Returns:
            The updated VideoFile object with the subclip flags set.
        """
        self.flags.update((("ss", start), ("t", duration)))
        return self

    @classmethod
    def from_imagefile(cls, imgpath: str, duration: float | str, fps: int) -> "VideoFile":
        """
        Creates a VideoFile object from an image file, looping it for the given
        duration and setting the frame rate.

        Args:
            imgpath: The path to the image file to use as a video.
            duration: The duration of the video in seconds.
            fps: The frame rate of the video.

        Returns:
            A VideoFile object created from the image file.
        """
        c = cls(imgpath)
        c.flags["loop"] = 1
        c.flags["t"] = duration
        c.flags["r"] = fps
        return c

    def get_size(self) -> tuple[int, int]:
        """
        Retrieves the resolution (width and height) of the video file.

        Uses FFprobe to extract the width and height of the first video stream
        in the video file.

        Returns:
            tuple[int, int]: A tuple containing the width and height of the video.
        """
        data = ffprobe(
            self.filepath,
            (
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=width,height",
            ),
        )["streams"][0]
        return data["width"], data["height"]

    def get_duration(self) -> float:
        """
        Retrieves the duration of the video file.

        Uses FFprobe to extract duration the first video stream
        in the video file.

        Returns:
            Duration in seconds.
        """
        data = ffprobe(
            self.filepath,
            (
                "-v",
                "error",
                "-show_streams",
            ),
        )[
            "streams"
        ][0]
        return float(data["duration"])

    def __repr__(self) -> str:
        return f"<VideoFile filepath={(self.filepath)}>"
