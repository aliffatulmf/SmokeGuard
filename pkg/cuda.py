import torch


def get_device() -> str:
    total_devices = torch.cuda.device_count()
    return ",".join([f"cuda:{i}" for i in range(total_devices)])