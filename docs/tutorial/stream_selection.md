# Stream Selection

A media file can hold **multiple streams** (video, audio, subtitles, attachments, data). Normally, FFmpeg auto-selects “the best” video + audio, but sometimes you need direct control — e.g. pick the second audio track or ignore thumbnail streams.


We can select by doing:
```py
audio_stream = clip.get_stream(stream_index=1, stream_name="a")
```

---

## Under the hood

When you call **`get_stream`**:

* The library creates a `StreamSpecifier` object.
* Its **parent** is the current input (`VideoFile` / `InputFile`).
* The object stores the requested **type** (`a`, `v`, `s`, etc.) and **index**.
* During **command generation**, it expands into an FFmpeg `-map` expression (like `0:a:1`).

!!! Warning
    Importantly, this step does **not** check if the stream really exists. If the specifier is invalid, FFmpeg itself will fail later when you run the pipeline.

---

## Validation differences

* `get_stream` → **unsafe**, no validation, just builds a specifier.
* `__getitem__` → **validated**: the library checks metadata to ensure the stream exists before returning it.
* `__iter__` → can use **`ffprobe`** under the hood to walk through all streams in the file. This gives you a safe, iterable view of what streams are actually present.

So you pick the right tool depending on your trade-off between **speed** (no validation) and **safety** (validated with `ffprobe`).

---

## When to use

* **Use `get_stream`** when you want lightweight, direct control and already know what streams exist.
* **Use `__getitem__`** when you want validation and prefer an error earlier in Python instead of during FFmpeg execution.
* **Use `__iter__`** when you want to inspect or enumerate all streams (e.g. to build a UI that lists tracks, or to dynamically pick streams).

---

📖 For the exact function signature and return type, see the [API Reference → Stream Selection](/ffmpeg-studio/api_reference/inputs/#ffmpeg.inputs.VideoFile).
