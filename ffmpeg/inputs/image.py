from ..ffprobe.ffprobe import ffprobe
from .base_input import BaseInput


class ImageFile(BaseInput):
    """
    A class representing a Image file that can be processed with FFmpeg.

    This class provides methods for interacting with a Image file, such as
    building FFmpeg input flags
    """

    def __init__(self, filepath: str) -> None:
        """
        Initializes the ImageFile object with the specified file path.

        Args:
            filepath (str): The path to the image file to be processed.
        """
        super().__init__(stream_type="v") # Images are treated as video streams in ffmpeg
        self.filepath = filepath

    def build_input_flags(self) -> list[str]:
        """
        Builds the FFmpeg input flags for the video file.

        This method constructs the FFmpeg command line input flags to specify
        the video file to be processed.

        Returns:
            list[str]: A list of input flags for FFmpeg, including the file path.
        """
        command = self.build()
        command.extend(["-i", self.filepath])
        return command

    def get_size(self) -> tuple[int, int]:
        """
        Retrieves the resolution (width and height) of the image file.

        Uses FFprobe to extract the width and height of the first image stream
        in the image file.

        Returns:
            tuple[int, int]: A tuple containing the width and height of the image.
        """
        data = ffprobe(
            self.filepath,
            (
                "-v",
                "error",
                "-show_entries",
                "stream=width,height",
            ),
        )["streams"][0]
        return data["width"], data["height"]

    def __repr__(self) -> str:
        return f"<ImageFile filepath={self.filepath}>"
