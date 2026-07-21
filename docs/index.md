---
title: Python FFmpeg library for video editing and audio processing
description: Learn how ffmpeg-studio helps Python developers build FFmpeg pipelines for video editing, audio mixing, subtitles, overlays, and media automation.
---

# FFmpeg-studio

**ffmpeg-studio** is a Pythonic interface to [FFmpeg](https://ffmpeg.org/) for developers who want to build powerful video and audio workflows without writing long shell commands. It is a practical choice for Python users working on media conversion, transcoding, overlays, subtitles, and batch processing.

## Why developers use ffmpeg-studio

- Build FFmpeg pipelines in Python with a readable and chainable API
- Create video editing workflows such as trimming, scaling, and overlaying
- Mix audio tracks, extract streams, and automate media processing jobs
- Work with filter graphs for subtitles, fades, crops, and other effects
- Generate FFmpeg commands programmatically for scripts and applications

## Key Features

- Clean, chainable API to compose FFmpeg commands
- Automatic escaping of command-line arguments
- Support for simple and advanced filter graphs
- Easy integration into larger video and audio processing workflows
- Built-in support for progress callbacks

## Start here

- [Installation](/ffmpeg-studio/installation)
- [Getting Started](/ffmpeg-studio/getting-started/)
- [Basic Usage](/ffmpeg-studio/basics/)
- [FFprobe and FFplay](#ffprobe-and-ffplay)

## FFprobe and FFplay

Alongside ffmpeg-studio, this toolkit can also include convenient wrappers for common FFmpeg companion tools.

### ffprobe

A Python wrapper for the ffprobe utility to extract metadata from media files and inspect streams.

### ffplay

A Python wrapper for ffplay for previewing media from Python-based workflows.