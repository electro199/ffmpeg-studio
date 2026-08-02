# ffmpeg-studio

> ffmpeg-studio is a Pythonic interface to FFmpeg for building and running FFmpeg commands programmatically, including complex filter graphs. It targets Python developers who need video/audio transcoding, overlays, subtitles, audio mixing, and batch media processing without hand-writing long shell commands or raw `filter_complex` strings.

ffmpeg-studio wraps ffmpeg, ffprobe, and ffplay with a chainable, type-hinted API. It automatically handles safe quoting/escaping, input/output stream mapping, and progress tracking via callbacks. Unlike simpler wrappers, it has first-class support for building long, multi-stage filter graphs (scaling, overlay, mixing, etc.) as composable Python objects instead of string concatenation.

Install: `pip install ffmpeg-studio` (requires FFmpeg installed separately and available on PATH).

## Docs

- [Home](https://electro199.github.io/ffmpeg-studio/): Overview, key features, and why developers use ffmpeg-studio.
- [Installation](https://electro199.github.io/ffmpeg-studio/installation/): How to install the package and FFmpeg itself on Windows, macOS, and Linux.
- [Getting Started](https://electro199.github.io/ffmpeg-studio/getting-started/): First steps and a minimal working example.
- [Basics](https://electro199.github.io/ffmpeg-studio/basics/): Core concepts and the general workflow for building FFmpeg pipelines.
- [FAQ](https://electro199.github.io/ffmpeg-studio/FAQ/): Frequently asked questions about installation, filter graphs, async support, and comparisons to alternatives.
- [ffmpeg-studio vs ffmpeg-python](https://electro199.github.io/ffmpeg-studio/vs-ffmpeg-python/): Feature-by-feature comparison of filter graphs, escaping, type hints, async support, and maintenance status.
- [Troubleshooting](https://electro199.github.io/ffmpeg-studio/troubleshooting/): Fixes for common errors — FFmpeg not found, missing filters, filter reuse bugs, "Argument list too long" on very large filter graphs, thread-safety, async ffprobe calls, and ffmpeg-python import conflicts.

## Tutorials

- [Input Types](https://electro199.github.io/ffmpeg-studio/tutorial/making_input/): The different ways to create inputs.
- [Input](https://electro199.github.io/ffmpeg-studio/tutorial/video_input/): Working with video input files.
- [Subclip](https://electro199.github.io/ffmpeg-studio/tutorial/subclip/): Trimming/subclipping media.
- [Stream Selection](https://electro199.github.io/ffmpeg-studio/tutorial/stream_selection/): Selecting specific audio/video streams from inputs.
- [Iterating Video Streams](https://electro199.github.io/ffmpeg-studio/tutorial/stream_iteration/): Iterating over multiple streams in a file.
- [Duration & Size](https://electro199.github.io/ffmpeg-studio/tutorial/media_info/): Reading media metadata via ffprobe.
- [Global Flags](https://electro199.github.io/ffmpeg-studio/tutorial/global_flags/): Setting global FFmpeg command flags.
- [Outputs](https://electro199.github.io/ffmpeg-studio/tutorial/output/): Configuring outputs, mapping, and per-output flags.

## Examples

- [Conversion](https://electro199.github.io/ffmpeg-studio/example/format_conversion/): Simple format/container conversion.
- [Merge Streams](https://electro199.github.io/ffmpeg-studio/example/merge_streams/): Combining a video stream from one file with an audio stream from another.
- [Mosaic](https://electro199.github.io/ffmpeg-studio/example/mosaic/): Building a video mosaic/grid layout with overlays.
- [Graph Diagram](https://electro199.github.io/ffmpeg-studio/example/graph_diagram/): Visualizing generated filter graphs.
- [Progress Bar](https://electro199.github.io/ffmpeg-studio/example/progress_bar/): Tracking encode progress with callbacks.
- [Text Fuzzing](https://electro199.github.io/ffmpeg-studio/example/text_fuzzing/): Simple text fuzzer to test escaping.

## API Reference

- [Index](https://electro199.github.io/ffmpeg-studio/api_reference/): API reference overview.
- [Inputs](https://electro199.github.io/ffmpeg-studio/api_reference/inputs/): Input classes (`InputFile`, `VideoFile`, `AudioFile`, `ImageFile`, etc.).
- [Filters](https://electro199.github.io/ffmpeg-studio/api_reference/filters/): Filter classes and the `apply`/`apply2` helpers for building filter graphs.

## Repository

- [GitHub](https://github.com/electro199/ffmpeg-studio): Source code, issues, and releases.
- [PyPI](https://pypi.org/project/ffmpeg-studio/): Package releases and install instructions.

## Optional

- License: GPL-3.0.
- Related terms: FFmpeg Python wrapper, Python FFmpeg complex filter graph, FFmpeg command builder Python, ffprobe Python wrapper, ffplay Python wrapper.