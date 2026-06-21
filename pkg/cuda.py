import torch


def get_device(nums=None):
    device_count = torch.cuda.device_count()
    if device_count == 0:
        return "cpu"

    if nums is None or len(nums) == 0:
        return "cuda:0"

    valid_nums = [num for num in nums if 0 <= num < device_count]
    if len(valid_nums) != len(nums):
        invalid_nums = set(nums) - set(valid_nums)
        raise ValueError(f"Invalid device numbers: {invalid_nums}. Valid device numbers are: {list(range(device_count))}")

    return f"cuda:{valid_nums[0]}"
