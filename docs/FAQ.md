---
title: FAQ
description: Frequently asked questions about ffmpeg-studio, the Pythonic FFmpeg wrapper — installation, requirements, complex filter graphs, async support, and how it compares to alternatives.
---

# FAQ

## General

**What is ffmpeg-studio?**

ffmpeg-studio is a Pythonic interface for building and running FFmpeg commands, including complex filter graphs, without hand-writing raw filter strings or shell commands.

---

**Do I need FFmpeg installed separately?**

Yes. ffmpeg-studio wraps the FFmpeg/ffprobe binaries — it does not bundle them. FFmpeg must be installed and available on your system `PATH`.

---

**What Python versions are supported?**

Python 3.11 and above.


---

**What license is ffmpeg-studio released under?**

ffmpeg-studio is licensed under GPL-3.0


## Installation

**How do I install ffmpeg-studio?**

```bash
pip install ffmpeg-studio
```


---


**How do I install FFmpeg itself?**

see the [Installation guide](/ffmpeg-studio/installation/)

---

**What's the minimum FFmpeg version required?**

ffmpeg-studio is tested with **FFmpeg 8 (full build)**. Some FFmpeg builds ship without certain filters or codecs — using the full/complete build is strongly advised to avoid missing-filter errors.

## Usage

**How do I convert a file from one format to another?**

See the [Format Conversion example](/ffmpeg-studio/example/format_conversion) — the `export()` function handles simple one-line conversions.

---

**How do I build a complex filter graph (overlays, scaling, stacking, etc.)?**

Filters are composed as plain Python objects via `apply()` — no manual escaping, quoting, or raw `filter_complex` string-building required. You write Python; ffmpeg-studio handles generating the correct FFmpeg filter graph syntax underneath. See the [Tutorials](../tutorial/making_input.md) and [Examples](../example/mosaic.md) sections for concrete graphs.


---

**Does ffmpeg-studio support async/await?**

Partially. Running FFmpeg itself supports async via `run_async()`. `ffprobe` calls (media info, duration, etc.) are currently synchronous only.


---

**Can I track progress during encoding?**

Yes, via a `progress_callback` passed to `run()`/`run_async()`. See the [Progress Bar example](/ffmpeg-studio/example/progress_bar).

---

**Does ffmpeg-studio support GPU/hardware-accelerated encoding?**

Yes, you can enable GPU acceleration (NVENC, QSV, VideoToolbox, etc.) by passing the relevant flags through the global flags function.

---


**Can I use ffmpeg-studio for live streaming (RTMP, HLS, etc.)?**

Yes, but there's no dedicated helper for it yet — you'd build the streaming workflow yourself using the existing input/output/flags API. No worked example is available at the moment.

---

**Is ffmpeg-studio thread-safe / safe to run multiple instances concurrently?**

No, Library is not thread safe yet i.e sharing FFmpeg object across thread is not recommended. Running multiple instances is supported while keeping the objects unique.


## Comparisons

**How is ffmpeg-studio different from ffmpeg-python?**

ffmpeg-studio focuses on developer experience beyond just wrapping FFmpeg's own features — for example, it integrates ffprobe directly into input objects, so you can inspect a file's streams/duration without a separate probe call. It also has type-hinted, composable filter graphs, and doesn't require manual escaping of filter strings.

ffmpeg-python is still widely used and has a large install base, but its last release was in 2019, and there are hundreds of open issues and pull requests with no recent activity.

---


**How does ffmpeg-studio compare to MoviePy?**

ffmpeg-studio aims to match MoviePy's ease of use without needing to learn FFmpeg's filter/escaping system — while running close to native FFmpeg speed, since it builds and runs real FFmpeg commands instead of processing frame-by-frame in Python. It covers the same core use cases MoviePy is used for (cutting, concatenation, compositing, effects, format conversion).

---

**Why not just use FFmpeg from the command line directly?**

Using FFmpeg from the command line is straightforward but error prone ffmpeg-studio solves these issues so you can focus on the workflow not FFmpeg edge cases.

## Project status

**Is ffmpeg-studio production-ready?**

ffmpeg-studio is actively used in production by early adopters, currently in beta

---

**Is ffmpeg-studio actively maintained?**

Yes. New feautes are actively being developed and bugs are getting fixed.

---


**How do I report a bug or request a feature?**

Open an issue on [GitHub](https://github.com/electro199/ffmpeg-studio/issues).

---

**How can I contribute?**

Open an issue on [GitHub](https://github.com/electro199/ffmpeg-studio/issues) and lets discuss the subject.