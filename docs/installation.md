---
title: Install ffmpeg-studio and FFmpeg
description: Install ffmpeg-studio and FFmpeg on Windows, Linux, or macOS to start building Python video editing and audio processing workflows.
---

## Install with pip

Install ffmpeg-studio using following command:

```sh
pip install ffmpeg-studio
```

!!! note
    This project does not install the FFmpeg binary automatically.

---

## Install FFmpeg

To run ffmpeg-studio successfully, you also need the FFmpeg command-line tools installed on your system.

Use any of these methods:

#### Windows

Using winget:

```sh
winget install --id=Gyan.FFmpeg  -e
```

OR download and install FFmpeg from official website:

1. Download the latest FFmpeg build from [Offcial Website](https://www.gyan.dev/ffmpeg/builds/).
2. Extract the archive and add the `bin` directory to your system `PATH`.

#### Linux

Using Apt

```sh
sudo apt install ffmpeg
```

#### MacOS

Using Homebrew:

```sh
brew install ffmpeg
```

## Verify installation

```sh
ffmpeg -version
```
