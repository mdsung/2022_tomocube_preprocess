import sys
from pathlib import Path

import numpy as np
import pandas as pd

from src.image import CropSize, Point, crop_arr, normalize_img


def get_output_numpy_path(raw_data_path: Path) -> Path:
    return Path(
        f"{str(raw_data_path.parent).replace('raw_numpy', 'input2')}/{raw_data_path.stem}.npy"
    )


def get_center_point(target_file: Path, metadata_path: Path) -> Point:
    df = pd.read_csv(metadata_path)
    result = df.loc[
        df["file_name"] == target_file.stem + ".tiff", ["x", "y", "z"]
    ].to_numpy()[0]
    return Point(int(result[0]), int(result[1]), int(result[2]))


def main():
    # target_file = "/home/data/tomocube/processed/raw_numpy/sepsis/20220614/20220614.163204.097.monocyte-201_RI Tomogram.npy"
    # center_point = Point(276 // 2, 276 // 2, 210 // 2)
    # crop_size = CropSize(64, 64, 64)
    input_path = Path(sys.argv[1])
    metadata_path = Path(sys.argv[2])
    crop_size = CropSize(int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))

    center_point = get_center_point(input_path, metadata_path)
    output_path = get_output_numpy_path(input_path)
    get_output_numpy_path(input_path).parent.mkdir(parents=True, exist_ok=True)

    arr = np.load(input_path)
    arr = normalize_img(arr)
    arr = crop_arr(arr, center_point, crop_size)

    np.save(output_path, arr)


if __name__ == "__main__":
    main()
