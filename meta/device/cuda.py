import logging

import torch


def GetDevice(device="cuda", gpu_id=0, verbose=False):
    if not isinstance(device, str):
        raise ValueError("Argument 'device' must be a string.")
    if not isinstance(gpu_id, int):
        raise ValueError("Argument 'gpu_id' must be an integer.")
    if not isinstance(verbose, bool):
        raise ValueError("Argument 'verbose' must be a boolean.")

    if device == "cuda" and torch.cuda.is_available():
        if gpu_id >= torch.cuda.device_count():
            raise ValueError(f"Invalid GPU id. There are only {torch.cuda.device_count()} GPU(s).")
        device_name = torch.cuda.get_device_name(gpu_id)
        if verbose:
            logging.info(f"Using {device.upper()}:{gpu_id} on {device_name}")
        return f"cuda:{gpu_id}", device_name
    else:
        from cpuinfo import get_cpu_info
        gci = get_cpu_info()
        if verbose:
            logging.info(f"Using {device.upper()} on {gci['brand_raw']}")
        return "cpu", gci["brand_raw"]
