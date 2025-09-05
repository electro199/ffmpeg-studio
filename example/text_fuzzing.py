"""
Fuzzed Text Sliding Video Generator using FFmpeg

This script generates a video with randomized fuzzed text appearing in short,
sliding time windows. Each fuzzed text sample is drawn onto a white background
video using FFmpeg's `drawtext` filter.

Key features:
- Random text is generated using special characters, whitespace, and punctuation.
- Each text appears for a brief duration, then slides to the next.


The purpose is to test and visualize how FFmpeg handles text rendering with
complex characters and escaping rules in filter graphs.

Output:
- A video `out.mp4` is produced showing 100 different fuzzed strings.

Requirements:
- ffmpeg in path.

Example use case:
- Testing FFmpeg drawtext escaping
- Visual inspection of character handling in subtitles or overlays
"""

import random
import string

from ffmpeg import FFmpeg, InputFile, Map, apply
from ffmpeg.filters import Text

# All special characters to fuzz
special_chars = r" []=;:\/()%'\n\""


# Generate fuzzed string
def fuzz_text(length=10):
    base = special_chars + string.ascii_letters + string.whitespace + string.punctuation
    return "".join(random.choice(base) for _ in range(length))


# Loop to run fuzz text
v = InputFile("color=white:500x300", f="lavfi", r=60)
for i in range(100):
    text_value = fuzz_text()
    print(f"Fuzzing with text: {repr(text_value)}")
    slide = 0.05
    start = i * slide
    end = start + slide
    v = apply(
        Text(text=text_value, y=0, x=0, color="red", fontsize=80).enable_between(
            round(start, 3), round(end, 3)
        ),
        v,
    )

f = FFmpeg()
f.output(Map(v), t=round(end, 3), path=f"out.mp4")
f.run()
