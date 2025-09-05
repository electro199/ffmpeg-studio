"""
Usage of callback function to make progress with tqdm
"""

from functools import partial
from ffmpeg import VideoFile, export
from tqdm import tqdm

# Total duration in seconds at export
duration = 5

# make subclip with from 0 to duration
clip = VideoFile(r"video.mp4").subclip(0, duration)


# this function will be called everytime
# it must take a atleast one or last arg (stats) of dictionary you can add as many arg before it
# duration is required to calculate the progress but you can skip it
# and indicate that process it runing and just print the stats
# all raised exception in this function will be ignored
# it must not update the stats dictionary
def update_progress(duration: float, pbar: tqdm, stats: dict):
    out_time_ms = stats.get("out_time_ms")
    if out_time_ms is None:
        return

    current_time = out_time_ms / 1_000_000
    pbar.n = min(current_time, duration)
    pbar.update(0)


# Create tqdm progress bar
pbar = tqdm(total=duration, unit="s", desc="Processing", leave=True)

# here we are setting args for callback stats like
# update_progress(duration, pbar)
# last arg will be added during runtime call
progress_callback = partial(update_progress, duration, pbar)

export(clip, path="out.mp4").run(progress_callback=progress_callback, progress_period=1)

pbar.close()
