# Outputs

Outputs in **ffmpeg-studio** define where and how your processed media is exported.
Every graph of filters and inputs eventually needs to be connected to one or more outputs.

An output usually specifies:

* The **stream** (image, audio, or video) to be written
* The **path** (file name or stream sink)
* Optional **encoding options** (format, codec, etc.)

```python
from ffmpeg import FFmpeg, VideoFile
from ffmpeg.filters import apply, Scale

video = VideoFile("input.mp4")
scaled = apply(Scale(1280, 720), video)

(
    FFmpeg()
    .output(scaled, path="out.mp4")
    .run()
)

# Results in:
# ffmpeg -hide_banner -y -loglevel error -i input.mp4 \
# -filter_complex [0]scale=width=1280:height=720[n0o0] \
# -map [n0o0] out.mp4
```

---

## Multiple Outputs

ffmpeg-studio supports **multiple outputs in a single command** by simply chaining additional `.output()` calls.

This is particularly useful if you want export export a section from large edits or to save intermediate results (like a scaled logo) while also producing the final composed video .

Exporting both the **final overlaid video** and the **scaled logo**:

```python
from ffmpeg import FFmpeg, InputFile, VideoFile
from ffmpeg.filters import apply, Scale, Overlay

# Load logo and scale it
logo = InputFile("image.png")
scaled_logo = apply(Scale(200, 200), logo)

# Load video and scale to HD
video = VideoFile("video.mp4")
scaled_video = apply(Scale(1920, 1080), video)

# Make Clones with Split filter
scaled_logo_1, scaled_logo_2 = apply2(Split(2), scaled_logo)

# Overlay logo on video
final_video = apply(Overlay(scaled_logo_1, 0, 0), scaled_video)


ffmpeg = FFmpeg()

    
# Export the water marked video
ffmpeg.output(final_video, path="out.mp4")
# Export the scaled logo at same time
ffmpeg.output(scaled_logo_2, path="scaled_logo.png")

ffmpeg.run()


# Results:
# ffmpeg -hide_banner -y -loglevel error -i image.png -i video.mp4 
# -filter_complex [0]scale=width=200:height=200[n0o0];
#                 [n0o0]split=2[n1o0][n1o1];
#                 [1]scale=width=1920:height=1080[n2o0];
#                 [n2o0][n1o0]overlay=x=0:y=0[n3o0] 
#
# -map [n3o0] out.mp4 -map [n1o1] scaled_logo.png
```

---

# Key Takeaways

* `.output()` can be called multiple times in the same command.
* This avoids running `ffmpeg` multiple times for related exports saving decoding/encoding cost.

!!! Warning 

    Re-using the same stream in more than one .output() without splitting can cause ffmpeg errors (e.g., “Stream [n0o0] already used”).

    If you need the same stream in multiple outputs, explicitly split it with the `Split` filter before mapping it to different outputs.