import sys
from pathlib import Path

import numpy as np
import numpy.typing as npt
import tifffile


def tiff_to_numpy(raw_data_path: Path):
    image = tifffile.imread(raw_data_path)
    return np.array(image, dtype=np.float32).transpose(1, 2, 0)


def get_output_numpy_path(raw_data_path: Path) -> Path:
    return Path(
        f"{str(raw_data_path.parent).replace('raw', 'processed/raw_numpy')}/{raw_data_path.stem}.npy"
    )


def main():
    print(sys.argv)
    raw_data_path = Path(sys.argv[1])
    output_data_path = get_output_numpy_path(raw_data_path)
    output_data_path.parent.mkdir(parents=True, exist_ok=True)
    assert raw_data_path.exists()

    arr = tiff_to_numpy(raw_data_path)
    np.save(output_data_path, arr)


if __name__ == "__main__":
    main()
