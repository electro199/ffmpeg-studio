"""
Custom exceptions for runtime errors in FFmpeg and FFprobe.

These exceptions are raised when subprocess calls to FFmpeg or FFprobe fail,
capturing both the error message and return code.
"""


class FFmpegException(Exception):
    """
    Exception raised when an FFmpeg command fails.

    Attributes:
        msg: The error message returned by FFmpeg.
        return_code: The process return code from FFmpeg.
    """

    def __init__(self, msg: str, return_code: int) -> None:
        """
        Initialize FFmpegException.

        Args:
            msg: Error message from FFmpeg.
            return_code: Return code from FFmpeg process.
        """
        self.msg = msg
        self.return_code = return_code

    def __str__(self) -> str:
        return f"FFmpegException Message:\n\n{self.msg}"


class FFmpegCompileError(Exception):
    def __init__(self, msg) -> None:
        """
        Exception raised when an FFmpeg command generation fails.

        Args:
            msg: Error message from FFmpeg.
            return_code: Return code from FFmpeg process.
        """
        self.msg = msg

    def __str__(self) -> str:
        return f"FFmpegCompileError Message:\n\n{self.msg}"


class FFprobeException(FFmpegException):
    """
    Exception raised when an FFprobe command fails.

    Inherits from FFmpegException and is specific to FFprobe failures.

    Attributes:
        msg (str): The error message returned by FFprobe.
        return_code (int): The process return code from FFprobe.
    """

    def __init__(self, msg: str, return_code: int) -> None:
        """
        Initialize FFprobeException.

        Args:
            msg: Error message from FFprobe.
            return_code: Return code from FFprobe process.
        """
        self.msg = msg
        self.return_code = return_code

    def __str__(self) -> str:
        return f"FFprobeException Message:\n\n{self.msg}"
