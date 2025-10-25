# Input

The ffmpeg takes input in `[-key value -i path]`, ffmpeg-studio will make a input with `InputFile` or `VideoFile`. Both of them are does same thing but with VideoFile it comes with addition features like:

- **subclip** that sets `-ss` and `-t` for seek start and duration repectively
- **from_imagefile** that sets `-t` for duration and enable `loop`.
- **general streams** like video, audio and subtitles that corresponds to `stream_name:v:n` in both filter and map context in command.

```python
from ffmpeg import InputFile, FileInputOptions

clip = InputFile("video.mp4", FileInputOptions(duration=10, frame_rate=24))
```

It will create this command piece by running `clip.build_input_flags()`.

```
['-t', '10', '-r', '24', '-i', 'video.mp4']
```


