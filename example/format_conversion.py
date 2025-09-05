"""
Example Convert Input from one format to another without any filter
"""

from ffmpeg import InputFile, export


export(
    InputFile(r"video.mp4"),
    path="out.mkv",
).run()
