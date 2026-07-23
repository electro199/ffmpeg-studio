---
title: ffmpeg-studio FAQ
description: Frequently asked questions about ffmpeg-studio, the Pythonic FFmpeg wrapper — installation, requirements, complex filter graphs, async support, and how it compares to alternatives.
---

# FAQ

## General

**What is ffmpeg-studio?**

ffmpeg-studio is a Pythonic interface for building and running FFmpeg commands, including complex filter graphs, without hand-writing raw filter strings or shell commands.

**Do I need FFmpeg installed separately?**

Yes. ffmpeg-studio wraps the FFmpeg/ffprobe binaries — it does not bundle them. FFmpeg must be installed and available on your system `PATH`.

**What Python versions are supported?**

Python 3.11 and above.

**What license is ffmpeg-studio released under?**

GPL-3.0-or-later.

<!--
TODO: If there's anything practical users should know about what GPL-3.0-or-later
means for their use case (e.g. commercial use, linking, distribution requirements),
add it here or link to a plain-language explainer. Not legal advice — just
whatever you want users to know upfront.
-->

## Installation

**How do I install ffmpeg-studio?**

```bash
pip install ffmpeg-studio
```

**How do I install FFmpeg itself?**

see the [Installation guide](/ffmpeg-studio/installation/)

**What's the minimum FFmpeg version required?**

ffmpeg-studio is tested with **FFmpeg 8 (full build)**. Some FFmpeg builds ship without certain filters or codecs — using the full/complete build is strongly advised to avoid missing-filter errors.

## Usage

**How do I convert a file from one format to another?**

See the [Format Conversion example](/ffmpeg-studio/example/format_conversion) — the `export()` function handles simple one-line conversions.

**How do I build a complex filter graph (overlays, scaling, stacking, etc.)?**

Filters are composed as plain Python objects via `apply()` — no manual escaping, quoting, or raw `filter_complex` string-building required. You write Python; ffmpeg-studio handles generating the correct FFmpeg filter graph syntax underneath. See the [Tutorials](../tutorial/making_input.md) and [Examples](../example/mosaic.md) sections for concrete graphs.


**Does ffmpeg-studio support async/await?**

Partially. Running FFmpeg itself supports async via `run_async()`. `ffprobe` calls (media info, duration, etc.) are currently synchronous only.


**Can I track progress during encoding?**

Yes, via a `progress_callback` passed to `run()`/`run_async()`. See the [Progress Bar example](/ffmpeg-studio/example/progress_bar).

**Does ffmpeg-studio support GPU/hardware-accelerated encoding?**

Yes, you can enable GPU acceleration (NVENC, QSV, VideoToolbox, etc.) by passing the relevant flags through the global flags function.


**Can I use ffmpeg-studio for live streaming (RTMP, HLS, etc.)?**

Yes, but there's no dedicated helper for it yet — you'd build the streaming workflow yourself using the existing input/output/flags API. No worked example is available at the moment.

**Is ffmpeg-studio thread-safe / safe to run multiple instances concurrently?**

<!--
TODO: Fill in based on actual behavior/testing. If untested, say so rather
than implying a guarantee.
-->

## Comparisons

**How is ffmpeg-studio different from ffmpeg-python?**

<!--
TODO: Short answer here, then link to the full comparison page once written
(the "vs ffmpeg-python" page discussed earlier). Keep this FAQ answer to
2-3 sentences and let the dedicated page carry the detail.
-->

**How does ffmpeg-studio compare to MoviePy?**

<!--
TODO: Fill in if you have a clear position — MoviePy is generally
positioned as higher-level/simpler but slower and less suited to complex
filter graphs, but confirm this matches your own comparison before publishing.
-->

**Why not just use FFmpeg from the command line directly?**

<!--
TODO: Optional — worth answering if you get this question often. Likely
angles: type safety, composability, avoiding shell-escaping bugs, easier
to build dynamic/programmatic pipelines.
-->

## Project status

**Is ffmpeg-studio production-ready?**

<!--
TODO: Be honest here — this affects adoption decisions. If it's beta,
say so and note what "beta" means in practice (API may change, etc.).
-->

**Is ffmpeg-studio actively maintained?**

<!--
TODO: Point to release cadence / changelog / last commit activity,
or just state your maintenance intentions plainly.
-->

**How do I report a bug or request a feature?**

Open an issue on [GitHub](https://github.com/electro199/ffmpeg-studio/issues).

**How can I contribute?**

<!--
TODO: Link to CONTRIBUTING if one exists, or outline the basic process
(fork, branch, tests, PR) if not.
-->