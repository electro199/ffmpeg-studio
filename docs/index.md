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

## Start here

New to ffmpeg-studio? Start with [Installation](/ffmpeg-studio/installation/), then [Getting Started](/ffmpeg-studio/getting-started/) and [Basics](/ffmpeg-studio/basics/) to learn the core concepts, or check the [FAQ](/ffmpeg-studio/FAQ/) for common questions.

The [Tutorials](/ffmpeg-studio/tutorial/making_input/) walk through input types, working with video input, trimming and subclipping, stream selection and iteration, reading media info, setting global flags, and configuring outputs.

The [Cookbooks](/ffmpeg-studio/cookbooks/) section has practical recipes such as [adding a watermark](/ffmpeg-studio/cookbooks/video/watermark/) and [resizing a video](/ffmpeg-studio/cookbooks/video/resize/), while [Examples](/ffmpeg-studio/example/format_conversion/) covers format conversion, merging video and audio, building a video mosaic, visualizing filter graphs, showing a progress bar, and fuzz-testing text rendering.

For full class and function documentation, see the [API Reference](/ffmpeg-studio/api_reference/), covering [Inputs](/ffmpeg-studio/api_reference/inputs/) and [Filters](/ffmpeg-studio/api_reference/filters/). ffprobe and ffplay wrappers are covered [below](#ffprobe-and-ffplay).