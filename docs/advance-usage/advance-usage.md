Lets see how everything works in ffmpeg-studio


---

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
    .output(final_video, path="out.mp4")
    .run()
)
# Results
# ffmpeg -hide_banner -y -loglevel error -i image.png -i video.mp4 \
# -filter_complex [0]scale=width=200:height=200[n0o0]; \
#                 [1]scale=width=1920:height=1080[n1o0];\
#                 [n1o0][n0o0]overlay=x=0:y=0[n2o0] \
#  -map [n2o0] out.mp4
```


# Map Flags

We also need to set `-map` flags when exporting like setting fps or bitrate to do that we can set them in `Map` context.

Use `suffix_flags` when a flags requires a suffix like `-r:1` or `-r:v:1` otherwise `kwargs` will catch all normal flags.

Example with both Mapped and Unmapped stream

```python
(
    FFmpeg()
    .output(
        Map(
            final_video,
            r=30,  # normal flag: set frame rate
            b="2M",  # normal flag: set bitrate
            suffix_flags={"r": 60}  # suffixed flag: set output 0 video stream to 60 fps
        ),
        path="out.mp4"
    )
    .output(scaled_logo, path="scaled_logo.png")
    .run()
)
```
