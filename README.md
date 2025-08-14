# FFmpeg-studio

[![PyPI](https://img.shields.io/pypi/v/ffmpeg-studio?color=blue&label=PyPI)](https://pypi.org/project/ffmpeg-studio/)
[![License](https://img.shields.io/github/license/electro199/ffmpeg-studio)](LICENSE)
[![Docs](https://img.shields.io/badge/📚_Documentation-online-blue)](https://electro199.github.io/ffmpeg-studio/)
[![GitHub stars](https://img.shields.io/github/stars/electro199/ffmpeg-studio?style=social)](https://github.com/electro199/ffmpeg-studio/stargazers)

ffmpeg-studio provides a Pythonic interface to FFmpeg, allowing users to construct and execute FFmpeg commands programmatically.

It simplifies and Handles:

- Complex filter generation
- All popular Filters and Baseclass for custom filters
- Safe quoting & escaping
- Input handling & stream selection
- Output mapping & stream selection
- Progress tracking with callbacks
- Allows direct flags in command.

## Installation

From PyPi

```sh
pip install ffmpeg-studio
```

From Source

```sh
pip install git+https://github.com/electro199/ffmpeg-studio.git
```

## Usage

ffmpeg-studio support complex Filters and can be used with [`apply`](https://electro199.github.io/ffmpeg-studio/api/#ffmpeg.filters.apply) or [`apply2`](https://electro199.github.io/ffmpeg-studio/api/#ffmpeg.filters.apply2), apply2 is for multioutput filters like `Split` and `Concat`.

```py
from ffmpeg import FFmpeg, InputFile, FileInputOptions, Map
from ffmpeg.filters import apply, Scale, Overlay

# set options
clip = InputFile("video.mp4", FileInputOptions(duration=10))
overlay = InputFile("overlay.png")

# apply scale filter on clip
upscaled_clip = apply(Scale(1440, 1920), clip)

# apply scale filter on overlay
overlay = apply(Scale(100, 100), overlay)

# apply overlay filter with overlay on upscaled_clip
upscaled_clip = apply(Overlay(overlay, x=0, y=10), clip)

# run command
ffmpeg = (
    FFmpeg().output(Map(upscaled_clip), path="out.mp4").run(progress_callback=print)
)
```

For simple media conversion :

```py
from ffmpeg.inputs import VideoFile
from ffmpeg import export

clip = VideoFile("video.mp4")

export(
   clip,
   path="out.mkv",
).run()

```

## Install FFmpeg

This project does not install ffmpeg utility automatically.

Verify ffmpeg is installed:

```sh
ffmpeg -version
```


### Windows

Using winget:

```sh
winget install --id=Gyan.FFmpeg  -e
```

or download and install FFmpeg from [FFmpeg official website](https://ffmpeg.org/download.html):

1. Download the latest FFmpeg build from [here](https://www.gyan.dev/ffmpeg/builds/).
2. Extract the archive and add the `bin` directory to your system `PATH`.

### macOS

Using Homebrew:

```sh
brew install ffmpeg
```

#### Linux

For Debian/Ubuntu:

```sh
sudo apt install ffmpeg
```