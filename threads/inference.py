import cv2

from meta.counter import Counter
from meta.counter.fps import FPS
from meta.counter.inference_time import InferenceTime
from meta.image.manipulation import frame_to_pixmap, resize_frame
from meta.io import CONFIG_READ, ConfigIO, ModelHub, load_source
from meta.model.path import model_path
from meta.signal import ParameterNamespace, SignalEmitter, SnapshotNamespace
from meta.thread import StoppableThread


class Inference(StoppableThread):
    def __init__(self, **kwargs):
        super().__init__()
        self.device = kwargs["device"]
        self.source = kwargs["source"]
        self.single = kwargs["single"]
        self.verbose = kwargs["verbose"]
        self.models = [model_path("weights/model.pt"), model_path("weights/general.pt")]

        self.emitter = SignalEmitter()
        self.model_hub = ModelHub()
        self.config = CONFIG_READ

        self.loaded_models = []
        self.load_model()
        print("success load model")
    
    def load_model(self):
        if self.single:
            # Load a single model instance
            self.loaded_models = [self.model_hub.load_model(self.models[0], "cuda", names=["rokok"])]
        else:
            # Handling for multiple model instances
            for i, model in enumerate(self.models):
                if i == 1:
                    kwgs = {
                        "confidence": 0.60,
                        "iou": 0.45,
                        "agnostic": False,
                        "max_det": 1000,
                        "multi_label": True,
                        "augment": False,
                        "amp": True,
                    }
                    self.loaded_models.append(self.model_hub.load_model(model, "cuda", **kwgs))
                    del kwgs
                else:
                    self.loaded_models.append(self.model_hub.load_model(model, "cuda", names=["rokok"]))
        
    def run(self):
        cap = load_source(self.source, self.verbose)
        print("success load source")
        
        fps = FPS()
        infer_time = InferenceTime()
        frames = Counter()
        
        while cap.isOpened() and not self._stop_requested:
            fps.start()

            obj_detected = 0
            retrieve, frame = cap.read()
            
            if not retrieve:
                break
            
            frames.add()

            for model in self.loaded_models:
                infer_time.start()
                preds = model(frame).pandas().xyxy
                infer_time.stop()
                
                for pred in preds:
                    if pred.empty:
                        continue
                    
                    obj_detected = len(pred)
                    for objs in pred.to_numpy():
                        xmin, ymin, xmax, ymax, conf, _, name = objs
                        xmin, ymin, xmax, ymax = map(int, [xmin, ymin, xmax, ymax])

                        text = f"{name} {round(conf * 100)}%"
                        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        tw, th = text_size[0] + 10, text_size[1] + 10

                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (66, 66, 255), 2)
                        cv2.rectangle(frame, (xmin, ymin), (xmin + tw, ymin - th), (66, 66, 255), -1)

                        cv2.putText(frame, text, (xmin, ymin - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                        if name == "rokok":
                            pixmap = frame_to_pixmap(resize_frame(frame, scale=0.4))
                            snap = SnapshotNamespace(
                                conf, self.config[ConfigIO.CONFIDENCE], self.config[ConfigIO.IOU], infer_time.stats, fps.stats, pixmap)
                            self.emitter.emit_snapshot_signal(snap)
            
            fps.stop()
            
            pixmap = frame_to_pixmap(resize_frame(frame, scale=0.5))
            self.emitter.emit_camera_signal(pixmap)
            
            params = ParameterNamespace(frames=frames.stats, fps=fps.stats, inference=infer_time.stats, total_object=obj_detected)
            self.emitter.emit_parameter_signal(params)
