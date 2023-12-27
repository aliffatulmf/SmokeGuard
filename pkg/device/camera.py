import cv2

from pkg.checker import is_source_available


class VideoCamera:
    def __init__(self, source=0, **kwargs):
        try:
            is_source_available(source)
        except Exception as e:
            raise Exception("The video source is not available.") from e
        
        self.index = source
        self.video = cv2.VideoCapture(source)
        for key, value in kwargs.items():
            if str(key).startswith("CAP_PROP_"):
                self.video.set(getattr(cv2, key), value)
    
    def __del__(self):
        self.video.release()
    
    def is_available(self):
        return self.video.isOpened()

    def read(self):
        return self.video.read()
        # success, image = self.video.read()
        # if not success:
        #     raise ValueError("Could not read from video device")
        # return success, image
    
    def show(self, name="Video", ordkey="q"):
        while True:
            success, image = self.read()
            if not success:
                raise ValueError("Could not read from video device")
            
            cv2.imshow(name, image)
            if cv2.waitKey(1) & 0xFF == ord(ordkey):
                break
