from pathlib import Path

import numpy as np
import pytest
from icecream import ic
from src.raw_numpy_to_input import (
    Point,
    get_center_point,
    get_output_numpy_path,
)


@pytest.fixture(scope="module")
def target_arr():
    return np.load(
        Path(
            "/data/tomocube/processed/raw_numpy/sepsis/20220614/20220614.163204.097.monocyte-201_RI Tomogram.npy"
        )
    )


def test_get_output_numpy_path():
    assert get_output_numpy_path(
        Path(
            "/data/tomocube/processed/raw_numpy/sepsis/20220614/20220614.163204.097.monocyte-201_RI Tomogram.npy"
        )
    ) == Path(
        "/data/tomocube/processed/input/sepsis/20220614/20220614.163204.097.monocyte-201_RI Tomogram.npy"
    )


def test_get_center_point():
    path = "/data/tomocube/processed/raw_numpy/sepsis/20220614/20220614.163204.097.monocyte-201_RI Tomogram.npy"
    assert get_center_point(
        Path(path), "data/processed/tomocube_metadata.csv"
    ) == Point(106, 123, 117)
