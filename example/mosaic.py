"""
Example of creating a mosaic of videos with Vstack and HStack filters
"""

import glob

from ffmpeg import FFmpeg, InputFile
from ffmpeg.filters import HorizontalStack, Scale, VerticalStack, apply, Split

# Get all mkv files in video folder
# Make sure you have some mkv files in the video folder
# Or change the path to your own mkv files
videos = glob.glob(r"Videos/*.mkv")

# Create mosaic of 4 videos
inputs = [apply(Scale(500, 500), InputFile(video)) for video in videos[:4]]

ff = FFmpeg()

# Stack first two videos and next two videos vertically
#
# Providing inputs directly to VerticalStack is also supported
vertical_stack_1 = apply(VerticalStack(inputs[0], inputs[1]))
# vertical_stack_1 = apply(Scale(500, 500), vertical_stack_1)

# Providing inputs via apply is also supported
vertical_stack_2 = apply(VerticalStack(inputs[2], end_on_shortest=True), inputs[3])
# vertical_stack_2 = apply(Scale(500, 500), vertical_stack_2)

grid = apply(HorizontalStack(vertical_stack_1, vertical_stack_2, end_on_shortest=True))

# Set maximum duration of output video
max_duration = 10
ff.output(
    grid,
    t=max_duration,
    path="grid.mp4",
)

# Run the ffmpeg command
ff.run(progress_callback=print)
