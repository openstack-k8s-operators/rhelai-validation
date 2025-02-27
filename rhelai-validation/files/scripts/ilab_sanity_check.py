import sys

import torch


def sanity_check():
    """
    A simple sanity check method.

    A simple sanity check method that uses the GPU to multiply two
    tensors and checks GPU memory usage.
    """
    # Check for GPU availability
    if not torch.cuda.is_available():
        print("ERROR: GPU not available")
        raise Exception()

    device = torch.device("cuda")
    initial_memory_allocated = torch.cuda.memory_allocated(0)
    initial_memory_reserved = torch.cuda.memory_reserved(0)
    print(f"Memory allocated before matrix multiplication: {initial_memory_allocated / 1e6} MB")
    print(f"Memory reserved before matrix multiplication: {initial_memory_reserved / 1e6} MB")

    # Create two large tensors
    size = (1000, 1000)
    tensor_a = torch.rand(size, device=device)
    tensor_b = torch.rand(size, device=device)
    # Perform matrix multiplication
    result = torch.matmul(tensor_a, tensor_b)

    final_memory_allocated = torch.cuda.memory_allocated(0)
    final_memory_reserved = torch.cuda.memory_reserved(0)
    print(f"Memory allocated after matrix multiplication: {final_memory_allocated / 1e6} MB")
    print(f"Memory reserved after matrix multiplication: {final_memory_reserved / 1e6} MB")

    print(f"Result shape: {result.shape}")

    # Assert the GPU was used
    assert initial_memory_allocated < final_memory_allocated
    assert initial_memory_reserved < final_memory_reserved


try:
    sanity_check()
    sys.exit(0)
except Exception:
    sys.exit(1)
