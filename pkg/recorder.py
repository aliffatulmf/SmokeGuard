import datetime
import os

import cv2


class Recorder:
    def __init__(self, output, format="video", fps=5, w=640, h=640):
        if not isinstance(output, str):
            raise ValueError("Output must be a string")
        if format not in ["video", "image"]:
            raise ValueError("Format must be 'video' or 'image'")
        if not isinstance(fps, int) or fps <= 0:
            raise ValueError("FPS must be a positive integer")
        if not isinstance(w, int) or w <= 0:
            raise ValueError("Width must be a positive integer")
        if not isinstance(h, int) or h <= 0:
            raise ValueError("Height must be a positive integer")

        self.output = output
        self.format = format
        self.fps = fps
        self.w = w
        self.h = h
        self.running = False
        self.frame_count = 0

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def start(self):
        if self.running:
            raise Exception("Recorder is already running")

        if self.format == "video":
            self.video = cv2.VideoWriter(
                f"{self.output}/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
                cv2.VideoWriter_fourcc(*"mp4v"),
                self.fps,
                (self.w, self.h),
            )
        elif self.format == "image":
            self.folder = f"{self.output}/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(self.folder, exist_ok=True)

        self.running = True

    def write(self, frame):
        if not self.running:
            raise Exception("Recorder has not started yet")

        try:
            if self.format == "video":
                self.video.write(frame)
            elif self.format == "image":
                cv2.imwrite(f"{self.folder}/frame_{self.frame_count}.png", frame)
                self.frame_count += 1
        except Exception as e:
            print(f"Failed to write frame: {e}")

    def release(self):
        if self.format == "video":
            self.video.release()
        elif self.format == "image":
            pass

        self.running = False