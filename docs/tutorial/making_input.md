# Inputs Types

Inputs are the **entry point** to every FFmpeg pipeline. They define *where your media comes from* — whether that’s a video file, audio file, image, or even a generated test pattern.

In `ffmpeg-studio`, inputs are represented by **Python classes**. These wrap FFmpeg’s `-i` flag and input-related options into safe, composable objects.

Inputs are the **foundation of processing** — every filter, effect, or output depends on them. By modeling inputs as classes, you get type safety, clean APIs, and reusable building blocks.

---

## Available Input Classes

| Class              | Purpose                                                                   | Typical Use Case                                                           |
| ------------------ | ------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **`VideoFile`**    | Video-specific input with helpers for trimming, resolution, and metadata. | Cutting video segments, accessing video/audio streams.                     |
| **`AudioFile`**    | Audio-only input with specialized handling for audio streams.             | Audio extraction, mixing, replacing tracks.                                |
| **`ImageFile`**    | Static image input.                                                       | Overlays, slideshows, or looping images as video.                          |
| **`VirtualVideo`** | Synthetic video sources using FFmpeg's built-in generators.               | Test patterns, color fills, gradients, fractals, programmatic backgrounds. |
| **`InputFile`**    | Generic input for any media file or URL supported by FFmpeg.              | Flexible option when no specialized class fits.                            |
| **`BaseInput`**    | Abstract parent class.                                                    | Used internally, not directly instantiated.                                |

---

## VideoFile

`VideoFile` is designed for working with **video files** that may also contain audio.
It provides shortcuts for trimming, seeking, and accessing streams without writing raw FFmpeg flags.
This makes it ideal for use cases like **cutting highlights**, re-encoding, or extracting video-only streams.

```python
from ffmpeg import VideoFile

# Trim between 2s and 6s
video = VideoFile("interview.mp4").subclip(2, 6)

# Extract just the video stream
stream = video.video
```

## 


---

## AudioFile

`AudioFile` focuses on **audio-only content**, giving fine-grained access to audio streams.
It helps simplify operations like trimming, replacement, or background music mixing.
You should use it when you want audio-specific handling instead of a generic file class.

```python
from ffmpeg import AudioFile

# Load audio and later mix it with another source
voiceover = AudioFile("narration.wav")
```

---

## ImageFile

`ImageFile` is used for **static images** when integrating them into video workflows.
It allows looping, setting frame rate, and duration to treat images like video streams.
Great for **posters, slideshows, or overlays** that need to behave like video clips.

```python
from ffmpeg import ImageFile, FileInputOptions

# Loop image for 4 seconds as 60fps
cover = ImageFile("poster.png", FileInputOptions(loop=True, duration=4, frame_rate=60))
```

---

## VirtualVideo

`VirtualVideo` creates **synthetic sources** using FFmpeg’s `lavfi` (filter graph) inputs and other formats.
This is useful when you don’t have a file but need **test footage, backgrounds, or effects**.
It supports generators like color fills, gradients, fractals, SMPTE test bars etc.

```python
from ffmpeg import VirtualVideo

# Solid red background
bg = VirtualVideo.from_color("red", width=1280, height=720, duration=5)

# Gradient animation
grad = VirtualVideo.from_gradients(720, 1280, duration=4, rate=30)

# Mandelbrot fractal animation
mandelbrot = VirtualVideo.from_mandelbrot(width=800, height=600, duration=3, rate=25)

# Test pattern (classic SMPTE color bars)
test = VirtualVideo.from_testsrc(640, 480, duration=2, rate=24)
```

---

## InputFile

`InputFile` is the **generic fallback** for any media source that FFmpeg can open.
It doesn’t enforce type restrictions, giving you maximum flexibility.
Use this when working with **URLs, streams, or uncommon formats** that don’t fit into specialized classes.

```python
from ffmpeg import InputFile

# Direct input with raw flags
file = InputFile("media.mkv", ss=10, t=5)

# Equivalent to:
# ffmpeg -ss 10 -t 5 -i media.mkv
```
