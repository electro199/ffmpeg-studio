---
title: Show a real-time progress bar for FFmpeg exports in Python
description: Use a progress callback with ffmpeg-studio to drive a tqdm progress bar and get live percentage updates while FFmpeg processes a video export.
---

# Show a real-time progress bar for FFmpeg exports in Python

When an FFmpeg export takes more than a second or two, a script that just sits there silently is hard to trust — is it hung, or actually working? ffmpeg-studio lets you pass a `progress_callback` into `run()` so you can surface live progress in a CLI, a log file, or, as shown here, a `tqdm` progress bar — instead of leaving users staring at a blank terminal during long exports.

## Example

```python title="example/progress_bar.py"
--8<-- "example/progress_bar.py"
```

## How it works

- `update_progress` is the callback FFmpeg invokes repeatedly during export. It must accept `stats` argument, which ffmpeg-studio passes in on every call.
- `duration` is the expected length (in seconds) of whatever you're exporting — used calculate a percentage. Here it's also passed to `subclip(0, duration)` to trim the clip, you can use know export length as duration.
- `functools.partial` pre-binds `duration` and `pbar` to `update_progress`, since FFmpeg only ever supplies `stats` at call time.
- `stats["out_time_ms"]` is the current output timestamp in microseconds despite the name — dividing by `1_000_000` converts it to seconds.
- `progress_period=1` controls how often (in seconds) the callback fires; lower it for smoother updates or raise it to reduce overhead.
- Exceptions raised inside the callback are swallowed by ffmpeg-studio, and the callback should treat `stats` as read-only.