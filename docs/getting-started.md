# Getting Started

General Flow of using ffmpeg-studio, it has three main components: 

- Input: Classes to handle different types of input files like video, audio, image, etc.
- Filters: Functions and classes to apply various filters to the input streams.
- Export: Functions to export the processed streams to output files.

## Input

In most cases, you will want to transform a file, and FFmpeg-Studio provides specialized classes to make input handling clear, consistent, and free from duplication.

Available classes for taking media are:

| Class              | Purpose                                                                   | Typical Use Case                                                           |
| ------------------ | ------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| [**`VideoFile`**]((/ffmpeg-studio/api_reference/inputs/#ffmpeg.inputs.VideoFile))    | Video-specific input with helpers for trimming, resolution, and metadata. | Cutting video segments, accessing video/audio streams.                     |
| [**`AudioFile`**]((/ffmpeg-studio/api_reference/inputs/#ffmpeg.inputs.AudioFile))    | Audio-only input with specialized handling for audio streams.             | Audio extraction, mixing, replacing tracks.                                |
| [**`ImageFile`**]((/ffmpeg-studio/api_reference/inputs/#ffmpeg.inputs.ImageFile))    | Static image input.                                                       | Overlays, slideshows, or looping images as video.                          |
| [**`VirtualVideo`**]((/ffmpeg-studio/api_reference/inputs/#ffmpeg.inputs.VirtualVideo)) | Synthetic video sources using FFmpeg's built-in generators.               | Test patterns, color fills, gradients, fractals, programmatic backgrounds. |
| [**`InputFile`**]((/ffmpeg-studio/api_reference/inputs/#ffmpeg.inputs.InputFile))    | Generic input for any media file or URL supported by FFmpeg.              | Flexible option when no specialized class fits.                            |

### Define input

Define  Input object like below this will make a object with path to the video.
This will not check if path is valid or not.

```python
from ffmpeg import VideoFile


clip = VideoFile("video.mp4")
clip = clip.subclip(1, 10)

```




Different ways input can be handled based on usecase

```python
from ffmpeg import InputFile, FileInputOptions, VideoFile

# if you know flags
InputFile("video.mp4", ss=1, t=10)

# same but easy usage with limited flags
InputFile("video.mp4", FileInputOptions(start_time=1, duration=10))

# same with VideoFile easiest
VideoFile("video.mp4").subclip(1, 10)

# Results
# ['-t', '10', '-ss', '1', '-i', 'video.mp4']
```

## Filters

A Filter is a component used to process and transform the input or its stream i.e audio from a video.

This library extensively handles filters with built classes.
filters can be used with [`apply`](/ffmpeg-studio/api_reference/api/#ffmpeg.filters.apply) or [`apply2`](/ffmpeg-studio/api_reference/api/#ffmpeg.filters.apply2),
apply2 is for multi output filters like Split and Concat.
apply function make new output node in filter graph to be used in filter again or to be written in to output file while maintaining source.

```py
clip = InputFile("image.png")
clip_scaled = apply(Scale(1000, 1000), clip)
```

!!! Warning
    Filters contain parent info they are not independent, do not reuse them in more then one apply function.
    If you want to reuse them create new instance with same arguments.

## Export
For straightforward exporting, ffmpeg-studio provides a convenient [`export`](/ffmpeg-studio/api_reference/api/#ffmpeg.ffmpeg.export) function.
This allows you to quickly export a single output file containing one or more streams.


Combine audio and video from files and output them to a single file.

This code extracts the **video** from video 1 and the **audio** from video 2, then exports them into a single output file `out.mp4`.

```py
from ffmpeg import VideoFile, export

export(
    VideoFile("video1.mp4").video,  # Video stream from video.mp4
    VideoFile("video2.mp4").audio,  # Audio stream(s) from video1.mp4
    path="out.mp4",  # Output path
).run()

# ffmpeg ... -i video1.mp4 -i video2.mp4 -map 0:v -map 1:a out.mp4
```

For more complex scenarios where you need to map multiple streams or have more control over the output, you can use the `Map` class and set settings such as bitrate or fps along with the `FFmpeg` class directly.

```py
from ffmpeg.inputs import VideoFile
from ffmpeg import FFmpeg, Map

FFmpeg().output(
    # Map video stream from video.mp4 with fps 30
    Map(VideoFile("video1.mp4").video, r=30),
    # Map(automatically added)  qaudio stream from video 2.
    VideoFile("video2.mp4").audio,
    path="out.mp4",  # Output path
).run()
# ffmpeg ... -i video1.mp4 -i video2.mp4 -map 0:v -r 30 -map 1:a out.mp4
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
    FFmpeg().output(clip, audio, path="out.mp4").run()
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
