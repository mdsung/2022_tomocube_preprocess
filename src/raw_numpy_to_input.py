import sys
from pathlib import Path

import numpy as np
import pandas as pd

from src.image import CropSize, Point, crop_arr, normalize_img


def get_output_numpy_path(raw_data_path: Path) -> Path:
    return Path(
        f"{str(raw_data_path.parent).replace('raw_numpy', 'input')}/{raw_data_path.stem}.npy"
    )


def get_center_point(target_file: Path, metadata_path: Path) -> Point:
    df = pd.read_csv(metadata_path)
    result = df.loc[
        df["file_name"] == target_file.stem + ".tiff", ["x", "y", "z"]
    ].to_numpy()[0]
    return Point(result[0], result[1], result[2])


def main():
    # input_path = Path(
    #     "/data/tomocube/processed/raw_numpy/igra/re_20220610/20220610.171502.673.CD8_2-090_RI Tomogram.npy"
    # )
    # crop_size = CropSize(64, 64, 64)
    # metadata_path = Path("data/processed/tomocube_metadata.csv")
    input_path = Path(sys.argv[1])
    metadata_path = Path(sys.argv[2])
    crop_size = CropSize(int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))

    center_point = get_center_point(input_path, metadata_path)
    output_path = get_output_numpy_path(input_path)
    get_output_numpy_path(input_path).parent.mkdir(parents=True, exist_ok=True)

    arr = np.load(input_path)
    arr = crop_arr(arr, center_point, crop_size)
    arr = normalize_img(arr)

    np.save(output_path, arr)


if __name__ == "__main__":
    main()
