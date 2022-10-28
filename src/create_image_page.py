import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def create_image_page(filename: Path):
    arr = np.load(filename)
    ## create a figure with 64(8x8) subplots
    for i in range(arr.shape[2]):
        plt.subplot(
            int(np.ceil(np.sqrt(arr.shape[2]))),
            int(np.ceil(np.sqrt(arr.shape[2]))),
            i + 1,
        )
        plt.imshow(arr[:, :, i])
        plt.axis("off")

    plt.suptitle(filename.name)
    plt.savefig(f"figure/{filename.stem}.png")


def main():
    filename = Path(sys.argv[1])
    create_image_page(filename)


if __name__ == "__main__":
    main()
