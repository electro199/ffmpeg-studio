---
title: Fuzz test FFmpeg drawtext escaping in Python
description: Stress-test FFmpeg's drawtext filter and character escaping rules by generating random special-character strings with ffmpeg-studio, rendered as a sliding-text video.
---

# Text Fuzzing

FFmpeg's `drawtext` filter has strict, easy-to-get-wrong escaping rules for special characters (quotes, brackets, colons, backslashes). This script stress-tests those rules by generating 100 random strings from special characters and whitespace, rendering each one briefly on screen, and sliding to the next.

It's useful for:

- Verifying ffmpeg-studio's automatic quoting/escaping holds up under adversarial input
- Visually inspecting how specific characters render (or fail to render) in `drawtext`
- Regression-testing filter graph generation when special characters are involved

![FFmpeg drawtext escaping fuzz test output](/ffmpeg-studio/assets/text-fuzzing-escaping-test.gif)

## Example

```python title="example/text_fuzzing.py"
--8<-- "example/text_fuzzing.py"
```

Each run generates a new set of random strings, so output will differ between runs. The GIF above shows one example pass.