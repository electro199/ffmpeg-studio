# Subclip

FFmpeg supports extracting a portion of a media file - a *subclip* - by seeking to a start time and optionally stopping at an end time. In `ffmpeg-studio` you can do the same from your high-level classes:

```python
VideoFile("path/to/video.mp4").subclip(start, end)
AudioFile("path/to/audio.mp3").subclip(start, end)
```

## Under The Hood

`subclip` set flags internally to be used at command generation to only requested time range of the original file. It does **not** modify the original file; it instructs FFmpeg to seek and only use the requested portion when you run the pipeline or export.

::: ffmpeg.inputs.VideoFile.subclip

## Examples

### Example - Python API

```python
from ffmpeg import VideoFile, export

# take 5..15 seconds of the video
sub = VideoFile("demo.mp4").subclip(5, 15)
export(sub, path="demo_subclip.mp4").run()
```

```python
from ffmpeg import AudioFile, export

# take from 1:00 to 2:00 of the audio
sub_audio = AudioFile("podcast.mp3").subclip(60, 120)
export(sub_audio, path="podcast_part.mp3").run()
```
