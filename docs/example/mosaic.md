---
title: Build a Video Mosaic Grid in Python
description: Combine multiple videos into a 2x2 mosaic grid using ffmpeg-studio's VerticalStack and HorizontalStack filters in Python.
---

# Video Mosaic

This example arranges four videos into a single 2x2 grid — think security-camera-style multi-view or a highlight reel showing several clips at once. It's built with ffmpeg-studio's `VerticalStack` and `HorizontalStack` filters, which map directly to FFmpeg's `vstack`/`hstack`, without you having to hand-write the filter graph string.

<!-- The approach: each video is scaled to a uniform size, two are stacked vertically to form a column, then the two columns are stacked horizontally to form the final grid.

![2x2 video mosaic grid generated with ffmpeg-studio](/ffmpeg-studio/assets/images/video-mosaic-grid.gif) -->

## Example

```python title="example/mosaic.py"
--8<-- "example/mosaic.py"
```

## How it works

- `Scale(500, 500)` normalizes every input to the same dimensions — mismatched sizes will fail or distort when stacked
- `VerticalStack` stacks two videos top-to-bottom into a column
- `HorizontalStack` places two columns side by side to complete the grid
- `end_on_shortest=True` stops the output once the shortest input in that stack finishes, instead of padding or erroring
- `t=10` caps the final output to 10 seconds regardless of source length

This pattern extends beyond a 2x2 grid — nest more `VerticalStack`/`HorizontalStack` calls to build 3x3 grids or asymmetric layouts.