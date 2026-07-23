"""
Example: build a 2x2 video mosaic (grid) using ffmpeg-studio's
VerticalStack and HorizontalStack filters.
"""

import glob

from ffmpeg import FFmpeg, InputFile
from ffmpeg.filters import HorizontalStack, Scale, VerticalStack, apply

# Grab up to 4 videos from a folder. Point this at your own directory.
videos = glob.glob(r"Videos/*.mkv")[:4]

if len(videos) < 4:
    raise ValueError(
        f"Need at least 4 videos to build a 2x2 mosaic, found {len(videos)}"
    )

# Scale each video down to a uniform 500x500 tile before stacking.
inputs = [apply(Scale(500, 500), InputFile(video)) for video in videos]

# Stack videos into two columns: [0] over [1], and [2] over [3].
left_column = apply(VerticalStack(inputs[0], inputs[1]))
right_column = apply(VerticalStack(inputs[2], inputs[3], end_on_shortest=True))

# Combine both columns side by side into a single 2x2 grid.
grid = apply(HorizontalStack(left_column, right_column, end_on_shortest=True))

ffmpeg = FFmpeg()
ffmpeg.output(grid, t=10, path="grid.mp4")  # cap output at 10 seconds
ffmpeg.run(progress_callback=print)
