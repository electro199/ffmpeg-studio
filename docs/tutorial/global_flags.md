# Global flags

Global flags are used change settings for whole runtime, you can use `add_global_flag` to set custom flags, These flags are automatic added duration command generation in `FFmpeg.compile()`:

- `-y` or `-n` to set overwrite outfile.
- `-loglevel error` to only read errors.
- `-hide_banner` to avoid extra pipe writes and cleaner output.

## Usage

The `add_global_flag` take raw flags with single value :

```python
ffmpeg = FFmpeg()
ffmpeg.add_global_flag("-recast_media")

## ffmpeg -recast_media -i ....
```

or key value pair :

```python
ffmpeg = FFmpeg()

ffmpeg.add_global_flag("-hwaccel_output_format", "d3d11")
ffmpeg.add_global_flag("-hwaccel", "d3d11va")
 
# ffmpeg -y -hwaccel_output_format d3d11 -hwaccel d3d11va -i ....
```
