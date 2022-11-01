import dataclasses
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

from src.file import read_target_list

# Objective: Extract the distribution metric from the array


@dataclass
class Metrics:
    target: Path
    value_mean: float
    value_std: float
    value_min: float
    value_25: float
    value_50: float
    value_75: float
    value_100: float


def load_file(path):
    return np.load(str(path))


def extract_distribution_metric(arr):
    return arr.mean(), arr.std(), np.percentile(arr, [0, 25, 50, 75, 100])


def main():
    targets = read_target_list()
    targets = [
        Path(str(target).replace("input", "raw_numpy")) for target in targets
    ]

    results = []
    for target in tqdm(targets):
        arr = load_file(target)
        (mean_value, std_value, percentiles) = extract_distribution_metric(arr)
        results.append(Metrics(target, mean_value, std_value, *percentiles))

    pd.DataFrame([dataclasses.asdict(result) for result in results]).to_csv(
        "data/processed/distribution_metrics.csv", index=False
    )


if __name__ == "__main__":
    main()
