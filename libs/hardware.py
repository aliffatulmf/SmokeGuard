import torch

from libs.logger import console


def get_device(verbose: bool = False):
    if torch.cuda.is_available():
        console.success("GPU found. Moving model to GPU")
        return "cuda"
    else:
        console.warning("GPU not found. Moving model to CPU")
        return "cpu"
