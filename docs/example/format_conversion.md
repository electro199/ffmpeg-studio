---
title: Convert video and audio formats
description: How to convert a media file from one format or container to another using ffmpeg-studio's Python interface to FFmpeg.
---

# Format Conversion

Converting a file between formats or containers — for example MP4 to MKV, or WAV to MP3 — is one of the most common FFmpeg tasks. ffmpeg-studio wraps this in a simple `export` call, so you don't need to hand-write the FFmpeg command.

## Example

```python title="example/format_conversion.py"
--8<-- "example/format_conversion.py"
```