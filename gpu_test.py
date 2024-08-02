import torch

if torch.cuda.is_available():
    print(f"CUDA is available. Using GPU: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available. Using CPU.")

# Get the current CUDA cache size
# cache_size = torch.cuda.memory_cached(device=torch.cuda.current_device())
# cache_size_mb = cache_size / (1024 ** 2)
#
# print(f"CUDA cache size: {cache_size_mb:.2f} MB")

# It will print out the GPU that you are using.