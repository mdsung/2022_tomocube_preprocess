from pathlib import Path

import pandas as pd

DATA_PATH = Path("/home/data/tomocube/raw/")


def get_target_files():
    df = pd.read_csv("data/processed/sepsis_meta.csv")
    df = df.loc[
        (df["quality"] == 0)
        & (df["image_type"] == "HOLOTOMOGRAPHY")
        & (~pd.isnull(df["x"]))
        & (df["file_name"].str.contains("CD4|CD8"))
    ]
    return df["file_name"].tolist()


def get_all_tiff_files_in_folder(path: Path) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "path": [p for p in path.glob("**/*.tiff")],
            "file_name": [p.name for p in path.glob("**/*.tiff")],
        }
    )


def main():
    all_tiff_files = get_all_tiff_files_in_folder(DATA_PATH)
    target_files = get_target_files()

    final_files = all_tiff_files.loc[
        all_tiff_files["file_name"].isin(target_files)
    ]

    target_list = (
        final_files["path"]
        .astype(str)
        .str.replace("raw", "processed/input")
        .str.replace("tiff", "npy")
        .to_list()
    )

    with open("data/processed/target_files.txt", "w") as f:
        f.write("\n".join(target_list))


if __name__ == "__main__":
    main()
