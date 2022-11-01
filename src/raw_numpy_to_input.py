import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import numpy.typing as npt
import pandas as pd
from icecream import ic


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
    result = arr[start_x:end_x, start_y:end_y, start_z:end_z]
    result = _padding_with_median(result, crop_size, np.median(arr))
    return result


def _get_start_point(anchor: int, center: int, crop_size: int):
    return max(anchor, center - crop_size // 2)


def _get_end_point(anchor: int, center: int, crop_size: int):
    return min(anchor, center + crop_size // 2)


def _padding_with_median(
    arr: npt.NDArray[np.float32], crop_size: CropSize, median_value: float
):
    ## padding with median when the size is smaller than crop_size
    if arr.shape[0] < crop_size.x:
        padding_x = np.zeros(
            (crop_size.x - arr.shape[0], arr.shape[1], arr.shape[2]),
            dtype=np.float32,
        )
        padding_x.fill(median_value)
        arr = np.concatenate([arr, padding_x], axis=0)
    if arr.shape[1] < crop_size.y:
        padding_y = np.zeros(
            (arr.shape[0], crop_size.y - arr.shape[1], arr.shape[2]),
            dtype=np.float32,
        )
        padding_y.fill(median_value)
        arr = np.concatenate([arr, padding_y], axis=1)
    if arr.shape[2] < crop_size.z:
        padding_z = np.zeros(
            (arr.shape[0], arr.shape[1], crop_size.z - arr.shape[2]),
            dtype=np.float32,
        )
        padding_z.fill(median_value)
        arr = np.concatenate([arr, padding_z], axis=2)
    return arr


def normalize_img(arr: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))


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
    ic(arr.shape)
    arr = crop_arr(arr, center_point, crop_size)
    ic(arr.shape)
    arr = normalize_img(arr)
    ic(arr.shape)

    np.save(output_path, arr)


if __name__ == "__main__":
    main()
