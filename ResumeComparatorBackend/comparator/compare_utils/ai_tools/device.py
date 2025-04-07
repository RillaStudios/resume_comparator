import torch

def get_device() -> int | str:
    """
    Returns the device type for PyTorch.

    Returns:
        0 if CUDA is available,
        "mps" if Metal Performance Shaders (MPS) is available,
        -1 if neither is available.

    @Author: IFD
    @Date: 2025-04-07
    """
    if torch.cuda.is_available():
        return 0
    elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
        return "mps"
    else:
        return -1