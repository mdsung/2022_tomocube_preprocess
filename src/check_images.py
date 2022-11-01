import concurrent.futures
from pathlib import Path

import numpy as np
from tqdm import tqdm

exist_results = []
shape_results = []
with open("data/processed/target_files.txt", "r") as f:
    targets = [Path(target) for target in f.read().split("\n")]

def check_target(target):
    if not target.exists():
        exist_results.append(target)
        return f"{target} does not exist\n"
    if not np.load(target).shape == (64, 64, 64):
        shape_results.append(target)
        return f"{target} is not 64x64x64\n"
    return ""


# with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
#     futures = [
#         executor.submit(check_target, target) for target in tqdm(targets)
#     ]
#     for future in concurrent.futures.as_completed(futures):
#         print(future.result(), end="")
for target in tqdm(targets):
    check_target(target)

with open('exist.txt', 'w') as f:
    f.write("\n".join([str(target) for target in exist_results]))

with open('shape.txt', 'w') as f:
    f.write("\n".join([str(target) for target in shape_results]))
