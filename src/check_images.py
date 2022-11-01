import concurrent.futures
from pathlib import Path

import numpy as np

exist_results = []
shape_results = []
with open("data/processed/target_files.txt", "r") as f:
    targets = [
        Path(target) for target in f.read().split("\n") if "sepsis" in target
    ]  # we dont want empty lines


def check_target(target):
    if not target.exists():
        return f"{target} does not exist\n"
    if not np.load(target).shape == (64, 64, 64):
        return f"{target} is not 64x64x64\n"
    return ""


with concurrent.futures.ProcessPoolExecutor(max_workers=18) as executor:
    futures = [executor.submit(check_target, target) for target in targets]
    for future in concurrent.futures.as_completed(futures):
        print(future.result(), end="")
