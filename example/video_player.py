import subprocess
import threading
import tkinter as tk

from PIL import Image, ImageTk  # pip install pillow

import ffmpeg


class FFmpegVideoPlayer:
    def __init__(self, root, video_path):
        self.root = root
        self.video_path = video_path
        self.label = tk.Label(root)
        self.label.pack()
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._play, daemon=True).start()

    def stop(self):
        self.running = False
        try:
            self.root.quit()  # stop Tk mainloop
            self.root.destroy()  # close window
        except:
            pass

    def _play(self):

        # Specify Input video 
        source = ffmpeg.VideoFile(self.video_path)

        # Scale Down Input video 
        width, height = 320, 320
        source = ffmpeg.apply(ffmpeg.filters.Scale(width, height), source.video)

        cmd = (
            ffmpeg.FFmpeg()
            .output(
                # Set format and pixel format
                ffmpeg.Map(source, f="image2pipe", pix_fmt="rgb24", vcodec="rawvideo"),
                # Take result into stdout
                path="-",
            )
            .compile()
        )

        # Run the command with stdout=subprocess.PIPE to capture the frames
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**8)


        frame_size = width * height * 3

        while self.running:
            raw_frame = process.stdout.read(frame_size)
            if not raw_frame:
                break

            image = Image.frombytes("RGB", (width, height), raw_frame)
            photo = ImageTk.PhotoImage(image)

            self.label.config(image=photo)
            self.label.image = photo

            self.root.update_idletasks()
            self.root.update()

        process.terminate()
        self.stop()  # << closes the app after video ends


if __name__ == "__main__":
    root = tk.Tk()
    root.title("FFmpeg Studio Tkinter Video Player")

    video_path = r"video.mp4"
    player = FFmpegVideoPlayer(root, video_path)

    player.start()
    root.protocol("WM_DELETE_WINDOW", player.stop)
    root.mainloop()
