# Iterating Video Streams

Working with media files often requires knowing exactly what streams are inside: multiple audio tracks, subtitles, or attachments. Instead of guessing or hardcoding stream indices, you can iterate over them directly.


When Iterating the we call the ffprobe to get all streams and give user list of `StreamSpecifier` with index and metadata from the ffprobe. This allow users flexiblity to use while processing streams.


## Loop over all Streams

Lets print all Streams and the codec_type

```python
clip = VideoFile("movie.mkv")

for stream in clip:
    print(s,  s.metadata['codec_type'])
```

Example output:

```
<StreamSpecifier stream_index=0 stream_name=None> video
<StreamSpecifier stream_index=1 stream_name=None> audio
<StreamSpecifier stream_index=2 stream_name=None> subtitle
```

## Extract All Audio Streams

Here  we checking if codec type is audio we are exporting stream into new file using multioutput feature and exporting at once.

```python

clip = VideoFile("movie.mkv")
audio_streams = [stream for stream in clip if stream.metadata["codec_type"] == "audio"]
ffmpeg = FFmpeg()

for a in audio_streams:
    ffmpeg.output(a, path=f"track_{a.stream_index}.mp3")

ffmpeg.run()

```

---

# Under the hood

* Iteration triggers a **probe** of the input file using **`ffprobe`**.
* The probe returns metadata about *all* streams in the file.
* Each stream is wrapped as a `StreamSpecifier` object with its index.
* This makes `__iter__` **validated and accurate** — you always get the real list of streams.

It’s slower because it calls `ffprobe`, but safer and more flexible.

