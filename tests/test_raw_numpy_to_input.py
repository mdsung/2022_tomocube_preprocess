from pathlib import Path

import numpy as np
import pytest
from src.raw_numpy_to_input import (
    CropSize,
    Point,
    crop_arr,
    get_center_point,
    get_output_numpy_path,
    normalize_img,
)


@pytest.fixture(scope="module")
def target_arr():
    return np.load(
        Path(
            "/home/data/tomocube/processed/raw_numpy/sepsis/20220614/20220614.163204.097.monocyte-201_RI Tomogram.npy"
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


def test_get_output_numpy_path():
    assert get_output_numpy_path(
        Path(
            "/home/data/tomocube/processed/raw_numpy/sepsis/20220614/20220614.163204.097.monocyte-201_RI Tomogram.npy"
        )
    ) == Path(
        "/home/data/tomocube/processed/input/sepsis/20220614/20220614.163204.097.monocyte-201_RI Tomogram.npy"
    )


def test_get_center_point():
    path = "/home/data/tomocube/processed/raw_numpy/sepsis/20220614/20220614.163204.097.monocyte-201_RI Tomogram.npy"
    assert get_center_point(Path(path)) == Point(106, 123, 117)
