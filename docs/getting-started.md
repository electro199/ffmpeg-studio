# Input

In most cases, you will want to transform a file, and FFmpeg-Studio provides specialized classes to make input handling clear, consistent, and free from duplication.

Available classes for taking media are:

- **InputFile**: A general-purpose input class for handling a wide range of media files. This is class can be used for stright forwad flag usage.

- **VideoFile**: A dedicated input type tailored for video sources. It makes it easier to configure video-specific parameters such as frame rate, resolution, and stream mapping. This is particularly useful when processing high-resolution video content or when multiple video streams need to be managed within the same pipeline.

- **ImageFile**: Designed for static image files, this class is ideal when building video slideshows, performing image-to-video conversions, or applying filters to single frames.

- **AudioFile**: A specialized class for audio-only inputs, enabling precise handling of audio streams. It provides straightforward access to audio-specific settings such as sample rate, channel layouts, and codec handling. This is useful for workflows involving audio extraction, mixing, or track replacement in multimedia projects.

- **VirtualVideo**: A powerful utility for generating synthetic video streams directly within the pipeline. This is especially useful for testing, debugging, or producing programmatically generated content such as blank backgrounds, color patterns, or animated test sources without relying on external media files.

**Usage:**

Different ways input can be handled based on usecase

```python
from ffmpeg import InputFile, FileInputOptions, VideoFile

# if you know flags
clip1 = InputFile("video.mp4", ss=1, t=10)

# same but easy usage with limited flags
clip = InputFile("video.mp4", FileInputOptions(start_time=1, duration=10))

# same with VideoFile easiest
clip = VideoFile("video.mp4").subclip(1, 10)

# Results
# ['-t', '10', '-ss', '1', '-i', 'video.mp4']
```

# Filters

A Filter is a component used to process and transform then input or its stream i.e audio from a video. This library extensively handles filters with built classes.
filters can be used with [`apply`](/ffmpeg-studio/api/#ffmpeg.filters.apply) or [`apply2`](/ffmpeg-studio/api/#ffmpeg.filters.apply2), apply2 is for multi output filters like Split and Concat. apply function make new output node in filter graph to be used in filter again or to be written in to output file while maintaining source.

**Usage:**

```py
clip = InputFile("image.png")
clip_scaled = apply(Scale(1000, 1000), clip)
```

# Export

For simple exporting ffmpeg-studio comes with an easy-to-use `export` function to export the single output with possibly multiple stream.

Example:

Combine audio and video from files and output them to a single file.

This code extracts the **video** from `video1.mp4` and the **audio** from `video2.mp4`, then exports them into a single output file `out.mp4`.

```py
from ffmpeg import VideoFile, export

export(
    VideoFile("video1.mp4").video,  # Video stream from video.mp4
    VideoFile("video2.mp4").audio,  # Audio stream from video1.mp4
    path="out.mp4",  # Output path
).run()

# ffmpeg ... -i video1.mp4 -i video2.mp4 -map 0:v -map 1:a out.mp4
```

Which is same as Using `FFmpeg()` with `Map` but in this way you can add flags per `Map` like encoding.

```py
from ffmpeg.inputs import VideoFile
from ffmpeg import FFmpeg, Map

FFmpeg().output(
    Map(VideoFile("video.mp4").video),  # Map video stream from video.mp4
    Map(VideoFile("video1.mp4").audio),  # Map audio stream from video1.mp4
    path="out.mp4",  # Output path
).run()
# ffmpeg ... -i video.mp4 -i video1.mp4 -map 0:v -map 1:a out.mp4
```

!!! tip

    This method provides a more **explicit** control flow where each stream is mapped individually. you can provide flags for `-map` context with both stream suffixed flag or without.

---

## Example

Lets make a video from a image with audio with

```py
from ffmpeg.ffmpeg import FFmpeg
from ffmpeg.inputs import FileInputOptions, InputFile
from ffmpeg.models.output import Map

# set options
clip = InputFile(
    "image.png",
    FileInputOptions(loop=True, duration=5, frame_rate=60),
)
audio = InputFile(
    "audio.mp3",
    FileInputOptions(duration=5),
)

# run command
ffmpeg = (
    FFmpeg().output(Map(clip), Map(audio), path="out.mp4").run()
)

# ffmpeg ... -t 5 -r 60 -loop 1 -i image.png -t 5 -i audio.mp3 -map 0 -map 1 out.mp4
```

Here we are using `InputFile` it is for generic input which are support by FFmpeg like path or url in combination with `FileInputOptions`
this provide useful flags that are applied to input in ffmpeg command.

The above code is easy to understand which works like:

- `loop=True` will make a infinite loop
- we set a `duration` so infinite loop can end
- then set `frame_rate` at 60

At end we make a `FFmpeg()` and add a output with two stream mapping. The `Map` add stream(s) to a output file in this way we can add multiple streams to one output.
