---
title: Visualize FFmpeg filter graphs in Python
description: Generate a diagram of your FFmpeg complex filter graph with ffmpeg-studio to understand and debug multi-stage video/audio pipelines before running them.
---

# Graph Diagram

When you're chaining several filters together — scaling, overlays, mixing, subtitles — it gets hard to keep the whole pipeline in your head. ffmpeg-studio can render your filter graph as a diagram, so you can see exactly how inputs, filters, and outputs connect before you run the command.

This is especially useful for:

- Debugging a filter graph that isn't producing the output you expect
- Understanding someone else's (or your future self's) pipeline
- Documenting complex, multi-input/multi-output workflows

![FFmpeg filter graph diagram generated with ffmpeg-studio](/ffmpeg-studio/assets/images/filter_graph.jpg)

## Example

```python title="example/graph_diagram.py"
---8<-- "example/graph_diagram.py"
```

Running this generates a visual representation of the filter graph:
