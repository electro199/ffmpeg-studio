---
title: Python FFmpeg Library for Video and Audio Processing
description: Home Page for ffmpeg-studio, a Python wrapper for Modern FFmpeg for building and running FFmpeg commands programmatically, including complex filter graphs.
---

# FFmpeg-studio

**ffmpeg-studio** is a modern [FFmpeg](https://ffmpeg.org/) Python wrapper for developers who want to build powerful video and audio workflows without writing long shell commands. It is a practical choice for Python users working on media conversion, transcoding, overlays, subtitles, and batch processing.

## Key Features

- Automatic escaping of command-line arguments
- Easily get media info and stream metadata
- Visualize filter graphs and FFmpeg commands
- Support for large filter graphs with multiple inputs and outputs
- Easy integration into larger video and audio processing workflows
- Built-in support for progress callbacks
- Typed every step of the way for better IDE support and code completion

## How does it compare?

Existing tool chains for FFmpeg in Python are either unmaintained, slow, or limited in scope. ffmpeg-studio is designed to be a modern, fast, and flexible alternative.

- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) works with filter objects with automatic escaping and full type hints, instead of chained `.filter()` calls and manual stream-label management on an unmaintained (2019 last commit).

- [MoviePy](https://github.com/singular-labs/singular-moviepy) is a high-level video editing library that wraps FFmpeg, but it is very slow for complex workflows. Currently it is unmaintained and has no type hints.

## Start here

New to ffmpeg-studio? Start with [Installation](/ffmpeg-studio/installation/), then [Getting Started](/ffmpeg-studio/getting-started/) and [Basics](/ffmpeg-studio/basics/) to learn the core concepts, or check the [FAQ](/ffmpeg-studio/FAQ/) for common questions.

The [Tutorials](/ffmpeg-studio/tutorial/making_input/) walk through input types, working with video input, trimming and subclipping, stream selection and iteration, reading media info, setting global flags, and configuring outputs.

The [Cookbooks](/ffmpeg-studio/cookbooks/) section has practical recipes such as [adding a watermark](/ffmpeg-studio/cookbooks/video/watermark/) and [resizing a video](/ffmpeg-studio/cookbooks/video/resize/), while [Examples](/ffmpeg-studio/example/format_conversion/) covers format conversion, merging video and audio, building a video mosaic, visualizing filter graphs, showing a progress bar, and fuzz-testing text rendering.

For full class and function documentation, see the [API Reference](/ffmpeg-studio/api_reference/), covering [Inputs](/ffmpeg-studio/api_reference/inputs/) and [Filters](/ffmpeg-studio/api_reference/filters/). ffprobe and ffplay wrappers are covered [below](#ffprobe-and-ffplay).