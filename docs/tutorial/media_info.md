# Duration & Size

Many inputs in `ffmpeg-studio` expose convenience methods to quickly inspect common properties like **duration** and **size**. These are thin wrappers around `ffprobe`, so you don’t need to manually parse JSON output.

---

## Duration

You can query the total playtime of a media file in **seconds (float)**.

```python
VideoFile("sample.mp4").get_duration()   # -> 125.38
AudioFile("audio.mp3").get_duration()     # -> 215.72
```

* [**VideoFile.get_duration()**](/ffmpeg-studio/api_reference/inputs/#ffmpeg.inputs.VideoFile.get_duration) → returns the full duration of the video.
* [**AudioFile.get_duration()**](/ffmpeg-studio/api_reference/inputs/#ffmpeg.inputs.AudioFile.get_duration) → returns the full duration of the audio.

---

## Size

For visual inputs, you can query the **frame size** in pixels as `(width, height)`.

```python
VideoFile("sample.mp4").get_size()       # -> (1920, 1080)
ImageFile("cover.jpg").get_size()        # -> (800, 800)
VirtualVideo("testsrc").get_size()       # -> (640, 480)
```

* [**VideoFile.get_size()**](/ffmpeg-studio/api_reference/inputs/#ffmpeg.inputs.VideoFile.get_size) → frame resolution of the video.
* [**ImageFile.get_size()**](/ffmpeg-studio/api_reference/inputs/#ffmpeg.inputs.ImageFile.get_size) → image resolution.
* [**VirtualVideo.get_size()**](/ffmpeg-studio/api_reference/inputs/#ffmpeg.inputs.VirtualVideo.get_size) → resolution of generated test video sources.

---

## Under the hood

These helpers internally call `ffprobe` with stream-level queries:

* **Duration** → reads `format.duration` and converts to `float`.
* **Size** → reads `stream.width` and `stream.height` from the first video stream.

This avoids you having to run something like:

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of json sample.mp4
```

or

```bash
ffprobe -v error -show_entries format=duration -of json song.mp3
```

Your code just calls `.get_duration()` / `.get_size()` directly.
