from pathlib import Path

import pytest
from src.tiff_to_numpy import get_output_numpy_path, tiff_to_numpy


@pytest.fixture(scope="module")
def rawdata_path():
    return Path(
        "/home/data/tomocube/raw/sepsis/20220614/20220614.163204.097.monocyte-201_RI Tomogram.tiff"
    )


def test_tiff_to_numpy(rawdata_path):
    arr = tiff_to_numpy(rawdata_path)
    assert arr.shape == (276, 276, 210)


def test_get_output_numpy_path(rawdata_path):
    assert get_output_numpy_path(rawdata_path) == Path(
        "/home/data/tomocube/processed/raw_numpy/sepsis/20220614/20220614.163204.097.monocyte-201_RI Tomogram.npy"
    )
