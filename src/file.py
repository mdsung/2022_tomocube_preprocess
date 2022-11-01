from pathlib import Path


def read_target_list():
    with open("data/processed/target_files.txt", "r") as f:
        return [
            Path(target) for target in f.read().split("\n")
        ]  # we dont want empty lines
