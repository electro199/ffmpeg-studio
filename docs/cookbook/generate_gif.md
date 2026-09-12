---
title: Convert a Video to a GIF in Python
description: Learn how to convert a video into a high-quality animated GIF in Python using ffmpeg-studio.
---

# Convert a Video to a GIF in Python

GIFs are useful for short animations, previews, demonstrations, reactions, and lightweight visual content. However, GIF has an important limitation: it supports a maximum of **256 colors per frame**, so a direct video-to-GIF conversion can produce poor colors or unnecessarily large files.

In this recipe, you'll learn how to create better GIFs with **ffmpeg-studio** by combining frame-rate reduction, scaling, palette generation, and palette-based dithering.

The same technique can be adapted to create small web previews, high-quality animations, or optimized GIFs for sharing.

## Table of Content

- [Convert a video into an animated GIF](/ffmpeg-studio/cookbook/generate_gif/#step-1-import-the-required-modules)
- [Select a specific section of a video](/ffmpeg-studio/cookbook/generate_gif/#convert-only-part-of-a-video)
- [Control the GIF frame rate](/ffmpeg-studio/cookbook/generate_gif/#step-3-reduce-the-frame-rate)
- [Resize the output while preserving its aspect ratio](/ffmpeg-studio/cookbook/generate_gif/#step-4-resize-the-video)
- [Create looping GIFs](/ffmpeg-studio/cookbook/generate_gif/#loop-the-gif)
- [Optimize GIF size and quality](/ffmpeg-studio/cookbook/generate_gif/#optimizing-gif-file-size)
- [Best Practices](/ffmpeg-studio/cookbook/generate_gif/#best-practices)
- [Troubleshooting](/ffmpeg-studio/cookbook/generate_gif/#troubleshooting)


## Prerequisites

Install ffmpeg-studio:

```bash
pip install ffmpeg-studio
```

You'll also need a video file such as:

```
your-video.mp4
```

<center> 
<a href="http://www.pexels.com/video/playing-catch-the-bait-with-a-cat-6864596/" target="_blank">
    <image src="/ffmpeg-studio/assets/images/cat_video_thumbnail.png" alt="text" style="height:400px; border-radius: 20px;"></image></a>
</center>
<center> 
    <a href="http://www.pexels.com/video/playing-catch-the-bait-with-a-cat-6864596/" target="_blank">Video by cottonbro studio from Pexels</a>
</center>


## Step 1: Import the required modules

Import the classes required to load the video, construct the GIF filter graph, and export the result.

```python
from ffmpeg import VideoFile, export
from ffmpeg.filters import FPS, Scale, SWSFlags, Split, PaletteGen, PaletteUse, apply, apply2
```

## Step 2: Load the video

Create a `VideoFile` reference to the source video.

```python
video = VideoFile("your-video.mp4")
```

!!! note

    `VideoFile` does not decode the entire video into memory. It represents the media source that will be used when FFmpeg executes the generated pipeline.

## Step 3: Reduce the frame rate

Most videos contain 24, 30, or 60 frames per second. Keeping all of those frames can make a GIF unnecessarily large.

For most GIFs, 10–15 FPS is a good starting point.

```python
video = apply(
    FPS(15),
    video
)
```

This converts the video stream to 15 frames per second.

!!! tip

    Start with **15 FPS** for a good balance between smoothness and file size. For smaller GIFs, try 10 FPS.

## Step 4: Resize the video

GIF file size increases rapidly with resolution. A 1920×1080 GIF is usually much larger than necessary.

Resize the video to a width of 640 pixels while automatically calculating the height.

```python
video = apply(
    Scale(640, -1),
    video
)
```

To use Lanczos scaling:

```python
video = apply(
    Scale(
        640,
        -1
    ).set_flag(SWSFlags.LANCZOS),
    video
)
```

The `flags` argument is passed directly to FFmpeg's `scale` filter.

!!! tip

    For web and chat GIFs, widths around **320–640 pixels** are often sufficient.

## Step 5: Generate a color palette

GIF supports only 256 colors, so simply encoding the video directly as a GIF can produce poor color reproduction.

FFmpeg provides the `palettegen` filter to analyze the video and generate an optimized palette.

```python
palette = apply(
    PaletteGen(),
    video
)
```

For example, you can explicitly limit the palette to 256 colors:

```python
palette = apply(
    PaletteGen(
        max_colors=256,
    ),
    video
)
```

You can also reduce the number of colors to produce a smaller GIF:

```python
palette = apply(
    PaletteGen(
        max_colors=128,
    ),
    video
)
```

!!! note

    256 colors provides the highest possible GIF color depth. Reducing the palette can decrease file size, but may introduce more visible color banding.

## Step 6: Use the palette

The generated palette needs to be provided to `paletteuse` along with the original processed video stream.

```python
gif_video = apply(
    PaletteUse(palette),
    video,
)
```

The resulting stream contains the video converted into a GIF-compatible 256-color representation.

The important relationship is:

```text
Processed Video ──────────────┐
                              ↓
                         PaletteUse
                              ↓
                           GIF Video
                              ↑
                              │
PaletteGen ← Processed Video ─┘
```

The palette is generated from the same processed video that is eventually passed to `paletteuse`.

## Step 7: Export the GIF

Export the resulting stream with a `.gif` extension.

```python
export(
    gif_video,
    path="output.gif",
).run()
```

FFmpeg will encode the resulting video stream as an animated GIF.

## Complete code example

This creates a 15 FPS GIF with a maximum width of 640 pixels, a 256-color palette, Lanczos scaling, and Sierra 2-4A dithering.
```python
from ffmpeg import VideoFile, export
from ffmpeg.filters import (
    FPS,
    Scale,
    PaletteGen,
    PaletteUse,
    apply,
)

video = VideoFile("your-video.mp4")

video = apply(
    FPS(15),
    video,
)

video = apply(
    Scale(
        640,
        -1
    ).set_flag(SWSFlags.LANCZOS),
    video,
)

palette = apply(
    PaletteGen(
        max_colors=256,
    ),
    video,
)

gif_video = apply(
    PaletteUse(
        palette,
        dither="sierra2_4a",
    ),
    video,
)

export(
    gif_video,
    path="output.gif",
).run()
```

## Tips

### Convert only part of a video

You usually don't want to convert an entire video into a GIF.

For example, to create a GIF from seconds 10–15, restrict the input before processing it.

```python
video = VideoFile(
    "your-video.mp4"
).subclip(start=0, duration=4)
```

Then apply the normal GIF pipeline:

```python
video = apply(
    FPS(15),
    video,
)

video = apply(
    Scale(640, -1).set_flag(SWSFlags.LANCZOS),
    video,
)

palette = apply(
    PaletteGen(max_colors=256),
    video,
)

gif_video = apply(
    PaletteUse(palette, dither="sierra2_4a"),
    video,
    
)

export(
    gif_video,
    path="clip.gif",
).run()
```

!!! tip

    Shorter GIFs are usually a much better optimization than aggressively reducing quality. If a GIF is too large, first reduce its duration.

### Control GIF quality

There are three particularly important parameters when optimizing GIFs:

```text
Frame rate
Resolution
Number of colors
```

For example:

```python
FPS(10)
Scale(480, -1)
PaletteGen(max_colors=128)
```

produces a significantly smaller GIF than:

```python
FPS(30)
Scale(1080, -1)
PaletteGen(max_colors=256)
```

A useful starting point is:

| Use case        |   FPS |   Width |  Colors |
| --------------- | ----: | ------: | ------: |
| Small preview   |  8–10 |     320 |     128 |
| Web GIF         | 10–15 |     480 | 128–256 |
| High quality    | 15–20 | 640–800 |     256 |
| Large animation |   20+ |    800+ |     256 |

These are starting points rather than strict requirements.

### Improve color quality with dithering

Because GIF has only 256 colors, some source colors cannot be represented exactly.

Dithering helps FFmpeg approximate those colors.

```python
PaletteUse(
    palette,
    dither="sierra2_4a",
)
```

Common choices include:

```text
bayer
heckbert
floyd_steinberg
sierra2
sierra2_4a
sierra3
burkes
atkinson
```

For example:

```python
gif_video = apply(
    PaletteUse(
        palette,
        dither="floyd_steinberg",
    ),
    video,
    
)
```

!!! tip

    `sierra2_4a` is a good general-purpose starting point. Different videos can benefit from different dithering algorithms, so experiment when visual quality is important.

### Use Bayer dithering

Bayer dithering provides additional control over the dithering pattern.

```python
gif_video = apply(
    PaletteUse(
        palette,
        dither="bayer",
        bayer_scale=3,
    ),
    video,
)
```

The `bayer_scale` value controls the Bayer dithering strength.

### Reduce the color palette

You don't have to use all 256 colors.

For a smaller GIF:

```python
palette = apply(
    PaletteGen(
        max_colors=128,
    ),
    video,
)
```

For an even smaller palette:

```python
palette = apply(
    PaletteGen(
        max_colors=64,
    ),
    video,
)
```

Reducing the palette is particularly useful for animations with simple colors, logos, UI recordings, or illustrations.

### Generate the palette from changing areas

`palettegen` can analyze frames using different statistics modes.

The default full-frame approach:

```python
PaletteGen(
    stats_mode="full",
)
```

You can also use:

```python
PaletteGen(
    stats_mode="diff",
)
```

`diff` focuses more heavily on pixels that change between frames.

This can be useful for animations with a mostly static background and a smaller moving object.

### Preserve transparency

GIF transparency is limited compared with formats such as PNG or WebP, but FFmpeg can reserve a palette entry for transparency.

```python
palette = apply(
    PaletteGen(
        reserve_transparent=True,
    ),
    video,
)
```

Then:

```python
gif_video = apply(
    PaletteUse(
        palette,
        alpha_threshold=128,
    ),
    video
)
```

!!! note

    GIF does not provide full 8-bit alpha transparency. Semi-transparent edges can therefore look different from the original video.

### Loop the GIF

If your output should loop indefinitely, pass the appropriate GIF loop option during export.

```python
export(
    gif_video,
    path="output.gif",
    loop=0,
).run()
```

For a non-looping GIF:

```python
export(
    gif_video,
    path="output.gif",
    loop=1,
).run()
```

The exact export options are passed through to FFmpeg.

## Presets 
### A small GIF preset

For a GIF intended for Discord, documentation, or a small web preview:

```python
from ffmpeg import VideoFile, export
from ffmpeg.filters import FPS, Scale, SWSFlags, PaletteGen, PaletteUse, apply


video = VideoFile("your-video.mp4")

video = apply(
    FPS(10),
    video,
)

video = apply(
    Scale(
        480,
        -1
    ).set_flag(SWSFlags.LANCZOS),
    video,
)

palette = apply(
    PaletteGen(
        max_colors=128,
    ),
    video,
)

gif_video = apply(
    PaletteUse(
        palette,
        dither="sierra2_4a",
    ),
    video,

)

export(
    gif_video,
    path="small.gif",
).run()
```

### A high-quality GIF preset

This produces a larger GIF but preserves considerably more motion and detail:

```python
from ffmpeg import VideoFile, export
from ffmpeg.filters import FPS, Scale, SWSFlags, PaletteGen, PaletteUse, apply

video = VideoFile("your-video.mp4")

video = apply(
    FPS(20),
    video,
)

video = apply(
    Scale(
        800,
        -1,
    ).set_flag(SWSFlags.LANCZOS),
    video,
)

palette = apply(
    PaletteGen(
        max_colors=256,
        stats_mode="full",
    ),
    video,
)

gif_video = apply(
    PaletteUse(
        palette,
        dither="sierra3",
    ),
    video,
)

export(
    gif_video,
    path="high-quality.gif",
).run()
```

## Optimizing GIF file size

If the resulting GIF is too large, change the parameters in this order:

### 1. Reduce duration

For example:

```text
10 seconds → 5 seconds
```

### 2. Reduce resolution

```python
Scale(640, -1)
```

to:

```python
Scale(480, -1)
```

### 3. Reduce frame rate

```python
FPS(15)
```

to:

```python
FPS(10)
```

### 4. Reduce colors

```python
PaletteGen(max_colors=256)
```

to:

```python
PaletteGen(max_colors=128)
```

This generally provides a better quality/size tradeoff than simply lowering every setting at once.

## Add other video filters

The GIF pipeline can be combined with other filters.

For example, crop the video before creating the GIF:

```python
video = apply(
    Crop(800, 800, 200, 0),
    video,
)

video = apply(
    Scale(480, -1),
    video,
)
```

Or add a watermark:

```python
video = apply(
    Overlay(
        logo,
        x="main_w-overlay_w-20",
        y="main_h-overlay_h-20",
    ),
    video,
)
```

Then generate the palette from the final processed video.

The general pattern is:

```text
Input
  ↓
Crop
  ↓
Watermark
  ↓
FPS
  ↓
Scale
  ↓
Palette generation
  ↓
Palette use
  ↓
GIF
```

!!! important

    Apply visual transformations **before** `PaletteGen`. The palette should describe the actual frames that will become the GIF.


## Understanding the filter graph

The complete GIF conversion is not simply:

```text
Video → GIF
```

A high-quality conversion uses a filter graph:

```text
                 ┌──→ PaletteGen ──→   Palette
                 │                        │
Video → FPS → Scale → Split ──────────────┤
                 │                        ↓
                 └──────────────────→ PaletteUse
                                           │
                                           ↓
                                         GIF
```

The video is first transformed into the desired frame rate and resolution.

The processed stream is then split:

```text
              Split
             /     \
            /       \
           ↓         ↓
    PaletteGen    PaletteUse
                     ↑
                     │
                 Palette
```

`PaletteGen` analyzes the frames and produces a palette. `PaletteUse` then uses that palette to convert the video frames into the limited color space supported by GIF.

This is why palette generation and palette use need to operate on the same processed video stream.


## Troubleshooting

Commom issues are answer:

### The GIF has poor colors

Use the palette workflow instead of directly encoding the video as GIF.

Make sure you're using:

```python
PaletteGen()
```

and:

```python
PaletteUse()
```

rather than simply exporting the original video.

### The GIF is too large

Reduce:

```python
FPS(15)
```

to:

```python
FPS(10)
```

and/or:

```python
Scale(640, -1)
```

to:

```python
Scale(480, -1)
```

You can also reduce the palette:

```python
PaletteGen(max_colors=128)
```

### The GIF looks jerky

Increase the frame rate:

```python
FPS(20)
```

or:

```python
FPS(24)
```

However, increasing FPS can significantly increase file size.

### The GIF has visible color banding

Try using all 256 colors:

```python
PaletteGen(max_colors=256)
```

and experiment with a different dithering algorithm:

```python
PaletteUse(
    palette,
    dither="sierra3",
)
```

### The GIF is blurry

Start with a higher-resolution source and scale it down.

For example:

```python
Scale(
    640,
    -1
).set_flag(SWSFlags.LANCZOS)
```

Avoid enlarging a low-resolution source.

### The GIF doesn't loop as expected

Explicitly specify the GIF loop behavior during export:

```python
export(
    gif_video,
    path="output.gif",
    loop=0,
).run()
```

## Best practices

- Keep GIFs short.
- Use **10–15 FPS** for most web GIFs.
- Keep the width around **320–640 pixels** unless higher resolution is necessary.
- Use `palettegen` + `paletteuse` for better color reproduction.
- Use 256 colors when quality is more important than size.
- Reduce colors to 128 or 64 for simple animations.
- Experiment with dithering for visually complex footage.
- Generate the palette **after** your other video filters.
- Use Lanczos when quality is more important than scaling speed.
- Consider WebP or MP4 for longer or higher-resolution animations.


## Related recipes

- Resize a video in Python
- Crop a video in Python
- Add a watermark to a video in Python
- Overlay one video on another
- Add text to a video
- Extract frames from a video
- Create a video thumbnail
