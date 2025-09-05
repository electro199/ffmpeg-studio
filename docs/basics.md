# Basics

# Overview

FFmpeg-studio is a command builder for FFmpeg.

The package works by creating Python objects to represent filters, streams, inputs, and other FFmpeg components. These objects store the necessary data and configurations. When you're ready to execute or compile the command, you can use `ffmpeg.run()` or `ffmpeg.compile()` to generate the complete FFmpeg command.

This approach makes it easier to escape and build complex FFmpeg commands programmatically, reducing the risk of syntax errors and improving maintainability.

It allows you to inspect metadata or other properties of existing files. For example, you can use `VideoFile.get_duration` to retrieve the duration of a video, `VideoFile.get_size` to get its dimensions, or iterate over a `VideoFile` object to access its streams.

# General Flow
For most part you will want to edit or create media files which always flow this pattern:

1. Create InputFile or VideoFile.

2. Optionally, trim the input files using `subclip` or `get_duration` methods or get specific streams like video or audio.

3. Apply filters like `Scale` or `Overlay` to these input files using `apply` or `apply2` functions.

4. Use the `FFmpeg` class to define the output file and any additional settings like metadata.

5. Finally, call the `run()` method on the `FFmpeg` instance to execute the command.

```py
from ffmpeg import FFmpeg, InputFile, FileInputOptions, Map
from ffmpeg.filters import apply, Scale, Overlay

# set options
clip = InputFile("video.mp4", FileInputOptions(duration=10))
overlay = InputFile("overlay.png")

# apply scale filter on clip
upscaled_clip = apply(Scale(1440, 1920), clip)

# apply scale filter on overlay
overlay = apply(Scale(100, 100), overlay)

# apply overlay filter with overlay on upscaled_clip
upscaled_clip = apply(Overlay(overlay, x=0, y=10), clip)

# run command
ffmpeg = (
    FFmpeg().output(upscaled_clip, path="out.mp4").run(progress_callback=print)
)
```