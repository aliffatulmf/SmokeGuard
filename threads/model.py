import torch


class ModelLoader:
    def __init__(self, path: str):
        super().__init__()

        self.model = torch.hub.load(
            "cache/yolov5",
            "custom",
            path=path,
            source="local",
            trust_repo=True,
            verbose=False,
        )

    def update(self, **kwargs):
        self.model.__dict__.update(kwargs)
