---
title: Trim and subclip video/audio
description: How to extract a portion of a media file by seeking to a start and end time using ffmpeg-studio's subclip method, without modifying the original file.
---

# Subclip

FFmpeg supports extracting a portion of a media file - a _subclip_ - by seeking to a start time and optionally stopping at an duration. In `ffmpeg-studio` you can do the same from your high-level classes:

```python
VideoFile("path/to/video.mp4").subclip(start, duration)
AudioFile("path/to/audio.mp3").subclip(start, duration)
```

## Under The Hood

`subclip` set flags internally to be used at command generation to only requested time range of the original file. It does **not** modify the original file; it instructs FFmpeg to seek and only use the requested portion when you run the pipeline or export.

::: ffmpeg.inputs.VideoFile.subclip

## Examples

Make a subclip starting from 5s and 15s duration after the starting point

```python
from ffmpeg import VideoFile, export

sub = VideoFile("demo.mp4").subclip(5, 15)
export(sub, path="demo_subclip.mp4").run()
```

Make a subclip starting from 1 minute and keep 2min duration after the starting point

```python
from ffmpeg import AudioFile, export

sub_audio = AudioFile("podcast.mp3").subclip(60, 120)
export(sub_audio, path="podcast_part.mp3").run()
```
