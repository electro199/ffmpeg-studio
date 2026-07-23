---
title: Merge video and audio from two different files with ffmpeg-studio
description: How to combine a video stream from one file and an audio stream from another into a single MP4 output using ffmpeg-studio's Python interface to FFmpeg.
---

# Merge Video and Audio

Sometimes the video and audio you need live in two separate files — for example, replacing a clip's original audio with a different track, or combining a silent screen recording with narration. ffmpeg-studio lets you pull a stream from each file and combine them into one output without hand-writing the FFmpeg mapping flags.

## Example

```python title="example/merge_streams.py"
--8<-- "example/merge_streams.py"
```

This grabs the video stream from `video1.mp4` and the audio stream from `video2.mp4`, then exports both into a single `out.mp4`.