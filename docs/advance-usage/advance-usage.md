Lets see how everything works in ffmpeg-studio

# Input 
The ffmpeg takes input in `[-key value -i path]`, ffmpeg-studio will make a input with `InputFile` or `VideoFile`. Both of them are does same thing but with VideoFile it comes with addition features like:

- **subclip** that sets `-ss` and `-t`  for seek start and duration repectively
- **from_imagefile**  that sets `-t`  for duration and enable `loop`.
- **general streams** like video, audio and subtitles that corresponds to `stream_name:v:n` in both filter and map context in command.

```python
from ffmpeg import InputFile, FileInputOptions

clip = InputFile("video.mp4", FileInputOptions(duration=10, frame_rate=24))
```

It will create this command piece by running `clip.build_input_flags()`.

```
['-t', '10', '-r', '24', '-i', 'video.mp4']
```




---
# Global flags
Global flags are used change settings for whole runtime, you can use `add_global_flag` to set custom flags, These flags are automatic added duration command generation in `FFmpeg.compile()`:

- `-y` or `-n` to set overwrite outfile 
- `-loglevel error` to only read errors
- `-hide_banner` to avoid extra pipe writes and cleaner output.

## Usage
The `add_global_flag` take raw flags example as:
```python
FFmpeg().add_global_flag("-recast_media")

## Results ffmpeg -recast_media -i ....
```
---
# Filters

Filters are way the ffmpeg allow media to be manipulated, ffmpeg-studio use [`apply`](/ffmpeg-studio/api/#ffmpeg.filters.apply) or [`apply2`](/ffmpeg-studio/api/#ffmpeg.filters.apply2), apply2 is for multi output filters. Filter output can be exported or further filtered.

## Usage

The [`apply`](/ffmpeg-studio/api/#ffmpeg.filters.apply) functions take Filter and then the input to be filtered

```python
apply(Filter, clip)
```

## Example
Lets make a video logo overlay both scaled.

```python

from ffmpeg import FFmpeg, Map, InputFile, VideoFile
from ffmpeg.filters import apply, Scale, Overlay


logo = InputFile(
    "image.png",
)

scaled_logo = apply(Scale(200, 200), logo)

video = VideoFile(
    "video.mp4",
)

scaled_video = apply(Scale(1920, 1080), video)

final_video = apply(Overlay(scaled_logo, 0, 0),scaled_video)


(
    FFmpeg()
    .output(Map(final_video), path="out.mp4")
    .run()
)
# Results 
# ffmpeg -hide_banner -y -loglevel error -i image.png -i video.mp4 \
# -filter_complex [0]scale=width=200:height=200[n0o0]; \
#                 [1]scale=width=1920:height=1080[n1o0];\
#                 [n1o0][n0o0]overlay=x=0:y=0[n2o0] \
#  -map [n2o0] out.mp4
```
# Multiple Outputs

ffmpeg-studio supports multiple output in single command by simply calling one more `output`. Lets use previous example. Here we are export the video and scaled logo

```python

from ffmpeg import FFmpeg, Map, InputFile, VideoFile
from ffmpeg.filters import apply, Scale, Overlay


logo = InputFile(
    "image.png",
)

scaled_logo = apply(Scale(200, 200), logo)

video = VideoFile(
    "video.mp4",
)

scaled_video = apply(Scale(1920, 1080), video)

final_video = apply(Overlay(scaled_logo, 0, 0), scaled_video)


(
    FFmpeg()
    .output(Map(final_video), path="out.mp4")
    .output(Map(scaled_logo), path="scaled_logo.png")
    .run()
)

# Results 
# ffmpeg -hide_banner -y -loglevel error -i image.png -i video.mp4
# -filter_complex [0]scale=width=200:height=200[n0o0]; \
#                 [1]scale=width=1920:height=1080[n1o0];\
#                 [n1o0][n0o0]overlay=x=0:y=0[n2o0]\
# -map [n2o0] out.mp4 
# -map [n0o0] scaled_logo.png
```

# Map Flags

We also need to set `-map` flags when exporting like setting fps or bitrate to do that we will set them in `Map` context

Use `suffix_flags` when a flags requires a suffix like `-r:1` or `-r:v:1` otherwise `kwargs` will catch all normal flags.


```python
(
    FFmpeg()
    .output(Map(final_video,), path="out.mp4")
    .output(Map(scaled_logo), path="scaled_logo.png")
    .run()
)

```

