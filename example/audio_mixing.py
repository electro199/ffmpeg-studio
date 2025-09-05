"""
Example Quick Start to merge video and audio from two files
"""

from ffmpeg.inputs import VideoFile
from ffmpeg import export

# Grab video from File
video_stream = VideoFile("video1.mp4").video

# Grab audio from another File
audio_stream = VideoFile("video2.mp4").audio

# Combine them together and export as mp4 
export(
    video_stream,
    audio_stream,
    path="out.mp4",
).run()
