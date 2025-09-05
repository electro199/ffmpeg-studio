from .base_options import BaseOptions
from typing import Optional


class FileInputOptions(BaseOptions):
    """
    Represents input options for FFmpeg's `-i` flag.

    This class allows users to specify various input-related parameters
    for FFmpeg command generation.

    Note:
        The types for flags like `duration` are int but ffmpeg can accept multiple formats. see [ffmpeg](https://ffmpeg.org/ffmpeg-utils.html#Time-duration)

    Example usage:
    ```python
    options = InputOptions(duration=10, start_time="00:00:05", format="mp4", frame_rate=30)
    ```
    """

    def __init__(
        self,
        duration: Optional[float] = None,
        start_time: Optional[float] = None,
        format: Optional[str] = None,
        codec: Optional[str] = None,
        frame_rate: Optional[float] = None,
        video_size: Optional[str] = None,
        pixel_format: Optional[str] = None,
        sample_rate: Optional[int] = None,
        audio_channels: Optional[int] = None,
        thread_queue_size: Optional[int] = None,
        itsoffset: Optional[float] = None,
        itsoverride: Optional[bool] = None,
        analyzeduration: Optional[int] = None,
        probesize: Optional[int] = None,
        rtbufsize: Optional[str] = None,
        re: Optional[bool] = None,
        accurate_seek: Optional[bool] = None,
        discard: Optional[str] = None,
        vsync: Optional[str] = None,
        async_audio: Optional[int] = None,
        fps_mode: Optional[str] = None,
        loop: Optional[bool] = None,
    ) -> None:
        super().__init__()
        """
        Initialize input options for FFmpeg.

        :param duration: Set the input duration (in seconds).
        :param start_time: Seek to a specific time in the input file (format: HH:MM:SS or seconds).
        :param format: Specify input format (e.g., "mp4", "avi").
        :param codec: Specify input codec (e.g., "h264", "aac").
        :param frame_rate: Set frame rate for the input (e.g., 30, 60).
        :param video_size: Set resolution (e.g., "1920x1080").
        :param pixel_format: Specify pixel format (e.g., "yuv420p").
        :param sample_rate: Set audio sample rate in Hz (e.g., 44100).
        :param audio_channels: Set number of audio channels (e.g., 2 for stereo).
        :param thread_queue_size: Set the thread queue size for input processing.
        :param itsoffset: Set input timestamp offset (in seconds).
        :param itsoverride: Override input timestamps.
        :param analyzeduration: Set maximum duration to analyze (in microseconds).
        :param probesize: Set maximum amount of data to probe (bytes).
        :param rtbufsize: Set real-time buffer size (e.g., "100M").
        :param re: Read input at native frame rate.
        :param accurate_seek: Enable accurate seeking.
        :param discard: Discard specific input streams (e.g., "none", "all").
        :param vsync: Set video sync method (e.g., "cfr", "vfr").
        :param async_audio: Set audio sync method.
        :param fps_mode: Set FPS mode (e.g., "passthrough", "cfr").
        :param loop: Enable Looping always use with duration (e.g., 1 for infinite loop, 0 no loop).
        
        Example usage:
        ```python
        options = InputOptions(duration=10, start_time="00:00:05", format="mp4", frame_rate=30)
        ```
        """

        if duration:
            self.kwargs.update({"t": duration})
        if start_time:
            self.kwargs.update({"ss": start_time})
        if format:
            self.kwargs.update({"f": format})
        if codec:
            self.kwargs.update({"c:v": codec})
        if frame_rate:
            self.kwargs.update({"r": frame_rate})

        if video_size:
            self.kwargs.update({"s": video_size})

        if pixel_format:
            self.kwargs.update({"pix_fmt": pixel_format})
        if sample_rate:
            self.kwargs.update({"ar": sample_rate})
        if audio_channels:
            self.kwargs.update({"ac": audio_channels})
        if thread_queue_size:
            self.kwargs.update({"thread_queue_size": thread_queue_size})
        if itsoffset:
            self.kwargs.update({"itsoffset": itsoffset})

        if analyzeduration:
            self.kwargs.update({"analyzeduration": analyzeduration})
        if probesize:
            self.kwargs.update({"probesize": probesize})
        if rtbufsize:
            self.kwargs.update({"rtbufsize": rtbufsize})

        if discard:
            self.kwargs.update({"discard": discard})

        if vsync:
            self.kwargs.update({"vsync": vsync})
        if async_audio:
            self.kwargs.update({"async": async_audio})
        if fps_mode:
            self.kwargs.update({"fps_mode": fps_mode})

        if loop:
            self.kwargs.update({"loop": int(loop)})

        if re:
            self.args.append("re")
        if accurate_seek:
            self.args.append("accurate_seek")
        if itsoverride:
            self.args.append("itsoverride")

    def add_flags(self, key, value):
        """
        Add other FFMPEG flags
        """
        self.kwargs.update(key=value)
