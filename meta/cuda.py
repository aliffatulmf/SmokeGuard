"""
Meta CUDA

This module contains utility functions for working with CUDA devices.
"""

import torch

# get the number of available CUDA devices
DETECTED_CUDA_DEVICES = torch.cuda.device_count()


def get_cuda_devices(device_specifier=None):
    """
    Returns the specified CUDA devices. If no specifier is provided, it returns all available CUDA devices.

    Args:
        device_specifier (int, list, range, optional): The specifier for the CUDA devices. It can be:

            - None: In this case, all available CUDA devices are returned.

            - int: The number of a specific CUDA device.

            - list: A list of numbers of specific CUDA devices.

            - range: A range of numbers of specific CUDA devices.

    Returns:
        torch.device or list of torch.device: The specified CUDA device(s). If no CUDA devices are available, it returns the CPU device.

    Raises:
        ValueError: If the device number exceeds the total number of CUDA devices.
        TypeError: If the type of device specifier is invalid.
        AssertionError: If the type of device specifier is not int, list, range, None.

    Example:
        >>> get_cuda_devices()
        [device(type='cuda', index=0), device(type='cuda', index=1)]
        >>> get_cuda_devices(0)
        device(type='cuda', index=0)
        >>> get_cuda_devices([0, 1])
        [device(type='cuda', index=0), device(type='cuda', index=1)]
        >>> get_cuda_devices(range(2))
        [device(type='cuda', index=0), device(type='cuda', index=1)]
    """
    assert isinstance(device_specifier, (int, list, range, type(None))), "Invalid type for device specifier."

    # if no CUDA devices are available, fallback to CPU
    if DETECTED_CUDA_DEVICES == 0:
        return torch.device('cpu')

    # if the argument is None, return all CUDA devices
    if device_specifier is None:
        return [torch.device(f'cuda:{i}') for i in range(DETECTED_CUDA_DEVICES)]

    # if the argument is a list, return CUDA devices whose numbers are in the list
    elif isinstance(device_specifier, list):
        for i in device_specifier:
            if i >= DETECTED_CUDA_DEVICES:
                raise ValueError("Device number exceeds the total number of CUDA devices.")
        return [torch.device(f'cuda:{i}') for i in device_specifier]

    # if the argument is a number and it is less than the total number of available CUDA devices
    elif isinstance(device_specifier, int) and device_specifier < DETECTED_CUDA_DEVICES:
        return torch.device(f'cuda:{device_specifier}')

    # if the argument is a range, return the CUDA devices whose numbers are within the range
    elif isinstance(device_specifier, range):
        return [torch.device(f'cuda:{i}') for i in device_specifier]
    else:
        raise TypeError("Invalid type for device specifier.")


def get_gpu_name(*indices):
    """
    Returns the name of the GPU given its device ID.

    Args:
        device_id (int, optional): The device ID of the GPU. Defaults to 0.

    Returns:
        str: The name of the GPU.

    Example:
        >>> get_gpu_name(0)
        'RTX 4090'
        >>> get_gpu_name(0, 1, 5)
        ['RTX A5500', 'Tesla T4', 'Tesla V100']
    """
    assert all(isinstance(idx, int) for idx in indices), "All indices must be integers."
    assert all(0 <= idx < DETECTED_CUDA_DEVICES for idx in indices), "Index out of range."

    # Create a list of GPU names for each valid index
    return [torch.cuda.get_device_name(i) for i in indices]


def get_all_gpu_names():
    """
    Returns the names of all available GPUs.

    Returns:
        list: A list of names of all available GPUs.

    Example:
        >>> get_all_gpu_names()
        [(0, 'Tesla K80'), (3, 'Tesla P100-PCIE-16GB')]
    """
    return [(i, torch.cuda.get_device_name(i)) for i in range(DETECTED_CUDA_DEVICES)]
