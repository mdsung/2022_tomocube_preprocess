import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import numpy.typing as npt
import pandas as pd


@dataclass
class Point:
    x: int
    y: int
    z: int

    def __post_init__(self):
        if not isinstance(self.x, int):
            self.x = int(self.x)
        if not isinstance(self.y, int):
            self.y = int(self.y)
        if not isinstance(self.z, int):
            self.z = int(self.z)


@dataclass
class CropSize:
    x: int
    y: int
    z: int

    def __post_init__(self):
        if not isinstance(self.x, int):
            self.x = int(self.x)
        if not isinstance(self.y, int):
            self.y = int(self.y)
        if not isinstance(self.z, int):
            self.z = int(self.z)


def crop_arr(
    arr: npt.NDArray[np.float32], center: Point, crop_size: CropSize
) -> npt.NDArray[np.float32]:

    size_x, size_y, size_z = arr.shape
    start_x = _get_start_point(0, center.x, crop_size.x)
    start_y = _get_start_point(0, center.y, crop_size.y)
    start_z = _get_start_point(0, center.z, crop_size.z)
    end_x = _get_end_point(size_x, center.x, crop_size.x)
    end_y = _get_end_point(size_y, center.y, crop_size.y)
    end_z = _get_end_point(size_z, center.z, crop_size.z)

    return arr[start_x:end_x, start_y:end_y, start_z:end_z]


def _get_start_point(anchor: int, center: int, crop_size: int):
    return max(anchor, center - crop_size // 2)


def _get_end_point(anchor: int, center: int, crop_size: int):
    return min(anchor, center + crop_size // 2)


def normalize_img(arr: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))


def get_output_numpy_path(raw_data_path: Path) -> Path:
    return Path(
        f"{str(raw_data_path.parent).replace('raw_numpy', 'input')}/{raw_data_path.stem}.npy"
    )


def get_center_point(target_file: Path) -> Point:
    df = pd.read_csv("data/processed/sepsis_meta.csv")
    result = df.loc[
        df["file_name"] == target_file.stem + ".tiff", ["x", "y", "z"]
    ].to_numpy()[0]
    return Point(result[0], result[1], result[2])


def main():
    # target_file = "/home/data/tomocube/processed/raw_numpy/sepsis/20220614/20220614.163204.097.monocyte-201_RI Tomogram.npy"
    # center_point = Point(276 // 2, 276 // 2, 210 // 2)
    # crop_size = CropSize(64, 64, 64)
    input_path = Path(sys.argv[1])
    crop_size = CropSize(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))

    center_point = get_center_point(input_path)
    output_path = get_output_numpy_path(input_path)
    get_output_numpy_path(input_path).parent.mkdir(parents=True, exist_ok=True)

    arr = np.load(input_path)
    arr = crop_arr(arr, center_point, crop_size)
    arr = normalize_img(arr)

    np.save(output_path, arr)


if __name__ == "__main__":
    main()
