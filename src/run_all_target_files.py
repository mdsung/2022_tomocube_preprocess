import concurrent.futures
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

from src.raw_numpy_to_input import CropSize, Point, crop_arr, get_center_point
from src.raw_numpy_to_input import get_output_numpy_path as get_input_numpy_path
from src.raw_numpy_to_input import normalize_img
from src.tiff_to_numpy import get_output_numpy_path as get_raw_numpy_path
from src.tiff_to_numpy import tiff_to_numpy


def get_targets():
    with open("data/processed/target_files.txt", "r") as f:
        targets = [
            target for target in f.read().split("\n")
        ]  # we dont want empty lines
    return targets


def get_raw_data_path(target_file_path):
    return Path(
        str(target_file_path)
        .replace("processed/input", "raw")
        .replace("npy", "tiff")
    )


def save_numpy(path, arr):
    np.save(path, arr)


def get_metadata():
    return pd.read_csv("data/processed/tomocube_metadata.csv")


def get_center_point(metadata, target_file):
    result = metadata.loc[
        metadata["file_name"] == target_file.stem + ".tiff", ["x", "y", "z"]
    ].to_numpy()[0]
    return Point(result[0], result[1], result[2])


def process_target(target_file, metadata):
    if target_file.exists():
        return f"{target_file} already exists"

    raw_data_path = get_raw_data_path(target_file)
    raw_arr, raw_numpy_path = _process_raw_numpy(raw_data_path)
    center_point = get_center_point(metadata, raw_numpy_path)
    input_arr, input_numpy_path = _process_input_numpy(
        raw_arr, raw_numpy_path, center_point
    )
    return f"{target_file} done"


def _process_raw_numpy(raw_data_path):
    raw_arr = tiff_to_numpy(raw_data_path)
    raw_numpy_path = get_raw_numpy_path(raw_data_path)
    raw_numpy_path.parent.mkdir(parents=True, exist_ok=True)
    save_numpy(raw_numpy_path, raw_arr)
    return raw_arr, raw_numpy_path


def _process_input_numpy(raw_arr, raw_numpy_path, center_point):
    input_numpy_path = get_input_numpy_path(raw_numpy_path)
    input_numpy_path.parent.mkdir(parents=True, exist_ok=True)

    input_arr = crop_arr(raw_arr, center_point, CropSize(64, 64, 64))
    input_arr = normalize_img(input_arr)
    save_numpy(input_numpy_path, input_arr)
    return input_arr, input_numpy_path


def main():
    targets = get_targets()
    metadata = get_metadata()
    targets = [
        Path(target)
        for target in targets
        if target
        != "/data/tomocube/processed/input/sepsis/20220530/20220530.151100.719.CD4-125_RI Tomogram.npy"
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        futures = [
            executor.submit(process_target, target, metadata)
            for target in targets
        ]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())

    # for target in tqdm(targets):
    #     if Path(target).exists():
    #         continue
    #     try:
    #         process_target(target, metadata)
    #     except Exception as e:
    #         print(e)
    #         with open("error_files.txt", "a") as f:
    #             f.write(str(target) + "\n")


if __name__ == "__main__":
    main()
