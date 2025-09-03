## FFMPEG command structure
The FFmpeg have very complex command structure the position of flags can effect the output come. The command is mainly consist of input which can be be media (file/link on internet/or any supported protocol that ffmpeg supports), then optional filter flag that tell how input should be manipulated then map flag to set which stream should be used in output either the input file and/or the modified stream the is generated after filtering

Lets see the command structure with examples:

1. ffmpeg command with single input and single output simplest form

    - structure:
        
        ```
        ffmpeg [options] [[infile options] -i infile]... [[outfile options] outfile]...
        ```

    - example with `-y` to overwrite the 
        
        ```
        ffmpeg -y -t 30 input_file_path.mp4  -r 24 output_file_path.mp4 
        ```

usage: `ffmpeg [options] [[infile options] -i infile]... [filter ]...  [-map [outfile options] outfile]...`

ffmpeg `[[infile options] -i infile] [filters] [-map flags outfile]...`


multiple input, filter