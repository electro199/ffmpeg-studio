from ..ffprobe.ffprobe import ffprobe
from .base_input import BaseInput


class AudioFile(BaseInput):
    """
    A class representing a Audio file that can be processed with FFmpeg.

    This class provides methods for interacting with a Audio file, such as
    building FFmpeg input flags
    """

    def __init__(self, filepath: str, **kwargs) -> None:
        """
        Initializes the AudioFile object with the specified file path.

        Args:
            filepath: The path to the audio file to be processed.
        """
        super().__init__(stream_type="a", **kwargs)
        self.filepath = filepath

    def _build_input_flags(self) -> list[str]:
        """
        Builds the FFmpeg input flags for the video file.

        This method constructs the FFmpeg command line input flags to specify
        the video file to be processed.

        Returns:
            list[str]: A list of input flags for FFmpeg, including the file path.
        """
        command = self._build()
        command.extend(["-i", self.filepath])
        return command

    def probe(self) -> dict:
        """
        Retrieves the duration of the audio file.

        Uses FFprobe to extract the stats of the in the audio file.

        Returns:
            dict: with all data from ffprobe.
        """
        data = ffprobe(
            self.filepath,
            ("-v", "error", "-show_streams", "-show_format"),
        )
        return data

    def get_duration(self) -> float:
        """
        Retrieves the duration of the audio file.

        Uses FFprobe to extract duration of the first audio stream
        in the audio file.

        Returns:
            float: duration in seconds.
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

    def subclip(self, start: float | str, duration: float | str) -> "AudioFile":
        """
        Defines a subclip from the Audio file by setting the start and duration.
        This will not make a new copy until exported.

        Args:
            start: The start time of the subclip.
            duration: The duration of the subclip.

        Returns:
            AudioFile: The updated AudioFile object with the subclip flags set.
        """
        self.flags.update((("ss", start), ("t", duration)))
        return self

    def __repr__(self) -> str:
        return f"<AudioFile filepath={self.filepath}>"
