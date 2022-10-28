import pandas as pd
from pathlib import Path
import tifffile
import numpy as np
from tqdm import tqdm
from dataclasses import dataclass


@dataclass
class Boundingbox:
    x: float
    y: float
    z: float

    def start_point(self, point: int, image_crop_size: int) -> int:
        point -= image_crop_size // 2
        point = max(point, 0)
        return int(point)

    def end_point(self, point: int, image_crop_size: int, max_size: int) -> int:
        point += image_crop_size // 2
        return int(min(point, max_size))

    def full_image(self, image: np.array, image_crop_size: int, image_crop_size2: int):
        full_array = image[
            self.start_point(self.x, image_crop_size) : self.end_point(
                self.x, image_crop_size, 276
            ),  # for indexing last point
            self.start_point(self.y, image_crop_size) : self.end_point(
                self.y, image_crop_size, 276
            ),  # for indexing last point
            self.start_point(self.z, image_crop_size2) : self.end_point(
                self.z, image_crop_size2, 210
            ),  # for indexing last point
        ]

        if full_array.shape == (image_crop_size, image_crop_size, image_crop_size2):
            return full_array

        median_filled_image = np.full(
            (image_crop_size, image_crop_size, image_crop_size2), np.median(full_array)
        )
        print(full_array.shape)

        x_shape = full_array.shape[0]
        y_shape = full_array.shape[1]
        z_shape = full_array.shape[2]

        start_x = (image_crop_size - x_shape) // 2
        start_y = (image_crop_size - y_shape) // 2
        start_z = (image_crop_size2 - z_shape) // 2

        end_x = image_crop_size - start_x
        end_y = image_crop_size - start_y
        end_z = image_crop_size2 - start_z

        end_x = end_x if x_shape % 2 == 0 else end_x - 1
        end_y = end_y if y_shape % 2 == 0 else end_y - 1
        end_z = end_z if z_shape % 2 == 0 else end_z - 1

        median_filled_image[start_x:end_x, start_y:end_y, start_z:end_z] = full_array
        return median_filled_image


def get_cropped_image(img: np.array, x_list, y_list, z_list):

    bbox = Boundingbox(x_list, y_list, z_list)

    return bbox.full_image(img, 64, 64)


def normalize_img(img):
    min = np.min(img)
    max = np.max(img)
    img = (img - min) / (max - min)
    return img


def main(path, metadata_path):

    metadata = pd.read_csv(metadata_path)  # x, y, z

    image = tifffile.imread(path)
    image = np.array(image)
    image = image.transpose(1, 2, 0)
    image = image.astype(np.float32)

    file_name = path.stem + path.suffix
    filter_metadata = metadata[metadata["file_name"].isin([file_name])]
    x = filter_metadata.loc[:, "x"].item()
    y = filter_metadata.loc[:, "y"].item()
    z = filter_metadata.loc[:, "z"].item()
    image = get_cropped_image(image, x, y, z)
    image = normalize_img(image)

    np.save(f"/home/data/tomocube/processed/{file_name}", image)


if __name__ == "__main__":

    DATA_PATH = Path(
        "/home/data/tomocube/raw/sepsis/20220614/20220614.163204.097.monocyte-201_RI Tomogram.tiff"
    )
    METADATA_PATH = "sepsis_meta.csv"

    main(DATA_PATH, METADATA_PATH)
