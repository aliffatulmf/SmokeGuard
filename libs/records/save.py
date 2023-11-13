import datetime

import cv2

filetime = (
    datetime.datetime.now()
    .__str__()
    .replace(" ", "_")
    .replace(":", "_")
    .replace(".", "_")
)


class VideoRecord:
    def __init__(self, fps: int = 24, width: int = 640, height: int = 480):
        self.fps = fps
        self.width = width
        self.height = height
        self.filename = (
            f"videos/record_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
        )
        self.writer = cv2.VideoWriter(
            self.filename,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height),
        )

    def write(self, frame):
        if self.writer is not None:
            self.writer.write(frame)
        else:
            raise ValueError("VideoWriter is not initialized")

    def end(self):
        if self.writer is not None:
            self.writer.release()
        else:
            raise ValueError("VideoWriter is not initialized")

    def __del__(self):
        self.end()
