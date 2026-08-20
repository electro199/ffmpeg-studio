---
title: Add a Watermark to a Video in Python
description: Learn how to add a watermark or logo to a video in Python using ffmpeg-studio. Overlay transparent PNG logos, position them anywhere in the frame, and export high-quality branded videos.
---

# Add a Watermark or Logo to a Video in Python

Adding a watermark or logo is one of the most common video editing tasks. Whether you're branding YouTube videos, protecting client previews, adding a company logo, or creating social media content, FFmpeg's powerful **overlay** filter makes the process both fast and efficient.

In this recipe, you'll learn how to overlay a transparent PNG logo onto a video using **ffmpeg-studio**, a Python interface for FFmpeg. The same approach works for channel branding, preview watermarks, company logos, and other static image overlays.

## What you'll learn

After completing this guide, you'll know how to:

- Overlay a PNG logo onto a video
- Position a watermark anywhere on the screen
- Resize the logo before applying it
- Preserve the original audio
- Export the final video using H.264

---

## Prerequisites

Install ffmpeg-studio:

```bash
pip install ffmpeg-studio
```

You'll also need:

- A video file (`.mp4`, `.mov`, `.mkv`, etc.)
- A logo or watermark image (PNG with transparency is recommended)

Example files:

```
your-video.mp4
your-logo.png
```

!!! tip
PNG images support transparency (alpha channel), making them ideal for logos and watermarks. JPEG images do not support transparent backgrounds.

---

# Step 1: Import the required modules

Import the classes required to load media files, apply filters, and export the final video.

```python
from ffmpeg import FFmpeg, ImageFile, VideoFile, Map, export
from ffmpeg.filters import Overlay, Scale, apply
```

---

# Step 2: Load the media files

Create file objects for both the video and the watermark image.

```python
video = VideoFile("your-video.mp4")
logo = ImageFile("your-logo.png")
```

!!! note
`VideoFile` and `ImageFile` only create references to your media. The files are **not decoded or loaded into memory** until FFmpeg starts processing the export.

This design allows even very large videos to be processed efficiently without consuming unnecessary RAM.

---

# Step 3: Resize the logo

Watermarks should usually occupy only a small portion of the frame.

For example, resizing a 2000×2000 logo down to 100×100 pixels keeps it visible without covering important video content.

```python
logo = apply(
    Scale(100, 100),
    logo
)
```

!!! tip
Larger isn't always better. A subtle watermark is usually more professional and less distracting.

---

# Step 4: Overlay the logo

Now place the resized logo onto the video.

```python
watermarked = apply(
    Overlay(
        logo,
        x=0,
        y=10,
    ),
    video
)
```

This places the logo:

- 0 pixels from the left
- 10 pixels from the top

The result is a new video stream containing the watermark.

---

# Common watermark positions

FFmpeg allows positions to be specified using either fixed pixel values or expressions.

| Position     | x                        | y                        |
| ------------ | ------------------------ | ------------------------ |
| Top Left     | `0`                      | `0`                      |
| Top Right    | `"main_w-overlay_w"`     | `0`                      |
| Bottom Left  | `0`                      | `"main_h-overlay_h"`     |
| Bottom Right | `"main_w-overlay_w"`     | `"main_h-overlay_h"`     |
| Center       | `"(main_w-overlay_w)/2"` | `"(main_h-overlay_h)/2"` |

For a small margin from the edge:

| Position     | x                       | y                       |
| ------------ | ----------------------- | ----------------------- |
| Top Right    | `"main_w-overlay_w-20"` | `20`                    |
| Bottom Right | `"main_w-overlay_w-20"` | `"main_h-overlay_h-20"` |
| Bottom Left  | `20`                    | `"main_h-overlay_h-20"` |

These expressions automatically adapt to videos of different resolutions.

---

# Step 5: Export the final video

Finally, export the processed video.

```python
export(
    watermarked,
    path="output.mp4",
).run()
```

Your output video will contain the original video with the watermark permanently embedded.

---

# Complete example

```python
from ffmpeg import ImageFile, VideoFile, export
from ffmpeg.filters import Overlay, Scale, apply

video = VideoFile("your-video.mp4")
logo = ImageFile("your-logo.png")

logo = apply(
    Scale(100, 100),
    logo
)

watermarked = apply(
    Overlay(
        logo,
        x="main_w-overlay_w-20",
        y="main_h-overlay_h-20",
    ),
    video
)

export(
    watermarked,
    path="output.mp4",
).run()
```

---

# How it works

Internally, ffmpeg-studio generates an FFmpeg **filter graph** using the `overlay` filter.

The processing pipeline is:

```
Video
      \
       Overlay Filter → Output Video
      /
Logo
```

The overlay filter combines two video streams:

1. The main video.
2. The watermark image.

Each frame of the video receives the logo at the specified coordinates before being encoded into the output file.

Because the watermark is applied during encoding, there is no need to manually edit every frame.

---

# Tips for better watermarks

- Use a transparent PNG for cleaner results.
- Leave a 10–30 pixel margin from the edges.
- Resize large logos before overlaying.
- Avoid covering subtitles or important content.
- Use high-resolution logos to prevent blurry scaling.
- Keep branding subtle—large opaque logos can distract viewers.

---

# Troubleshooting

### My logo appears too large

Reduce the size using the `Scale` filter.

```python
Scale(80, 80)
```

---

### My watermark has a white background

You're probably using a JPEG image.

Use a PNG with transparency instead.

---

### The logo is partially outside the video

Check your `x` and `y` coordinates.

Using expressions such as:

```text
main_w-overlay_w-20
```

automatically keeps the watermark inside the frame.

---

### The image looks blurry

Start with a higher-resolution logo and scale it down rather than enlarging a small image.

---

# Next steps

Now that you've learned how to overlay a static logo, you can explore more advanced compositing techniques:

- Overlay multiple logos or images
- Animate a watermark using timeline expressions
- Fade a logo in or out
- Add text overlays
- Overlay videos instead of images
- Create picture-in-picture effects

---

# Related recipes

- Resize a video in Python
- Add subtitles to a video
- Overlay one video on another
- Crop a video
- Blur a region of a video
- Add text to a video
