import torch


def detect_cuda(nums=None):
    if torch.cuda.is_available():
        if not nums or len(nums) == 0:
            return ",".join([f"cuda:{i}" for i in range(torch.cuda.device_count())])
        else:
            for num in nums:
                if num < 0 or num >= torch.cuda.device_count():
                    return ",".join(
                        [f"cuda:{i}" for i in range(torch.cuda.device_count())]
                    )

            return ",".join([f"cuda:{num}" for num in nums])
    else:
        return "cpu"

def detect_cuda_compact(nums=None):
    if not torch.cuda.is_available():
        return "cpu"
    
    device_count = torch.cuda.device_count()    

    if nums is None or len(nums) == 0:
        return "cuda:" + ",".join(map(str, range(device_count)))
    
    valid_nums = [num for num in nums if 0 <= num < device_count]
    if len(valid_nums) != len(nums):
        invalid_nums = set(nums) - set(valid_nums)
        raise ValueError(f"Invalid device numbers: {invalid_nums}. Valid device numbers are: {list(range(device_count))}")
    
    return "cuda:" + ",".join(map(str, valid_nums))

def get_device(nums=None):
    device_count = torch.cuda.device_count()
    if device_count > 0:
        if nums is None or len(nums) == 0:
            return "cuda:" + ",".join(str(i) for i in range(device_count))
        else:
            valid_nums = [num for num in nums if 0 <= num < device_count]
            if len(valid_nums) != len(nums):
                invalid_nums = set(nums) - set(valid_nums)
                raise ValueError(f"Invalid device numbers: {invalid_nums}. Valid device numbers are: {list(range(device_count))}")
            return "cuda:" + ",".join(str(num) for num in valid_nums)
    else:
        return "cpu"