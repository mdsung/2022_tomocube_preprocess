from pathlib import Path

import numpy as np
import pytest
from icecream import ic
from src.image import (
    CropSize,
    Point,
    _padding_with_median,
    crop_arr,
    normalize_img,
)


@pytest.fixture(scope="module")
def target_arr():
    return np.load(
        Path(
            "/data/tomocube/processed/raw_numpy/sepsis/20220614/20220614.163204.097.monocyte-201_RI Tomogram.npy"
        )
    )


def test_crop_arr(target_arr):
    assert crop_arr(
        target_arr, Point(276 // 2, 276 // 2, 210 // 2), CropSize(64, 64, 64)
    ).shape == (64, 64, 64)


def test_normalize_img():
    assert all(
        normalize_img(np.array([1, 2, 3], dtype=np.float32))
        == np.array([0, 0.5, 1], dtype=np.float32)
    )


def test__padding_with_median():
    arr = np.array(
        [
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[7, 8, 9], [10, 11, 12], [13, 14, 15]],
            [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
        ]
    )
    ic(arr)
    result = _padding_with_median(arr, CropSize(3, 3, 3), 10)
    ic(result.shape)
    assert result.shape == arr.shape
