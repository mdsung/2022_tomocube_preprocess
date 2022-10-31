import pickle
from functools import partial
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from yaml import Loader

from src.database import DBNAME, HOST, PASSWORD, PORT, USER, get_engine, get_sql

PROCESSED_DATA_PATH = Path("/data/tomocube/processed/input/")
SEPSIS_PATIENTS = {5, 6, 7, 8, 9, 10, 11}
HEALTHY_PATIENTS = {
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
}


def get_timepoint_patient_data(
    timepoint: int, patient_id: int, cell_type: str, metadata: pd.DataFrame
):
    group = f"{patient_id}-{timepoint}"
    folder_name = metadata.loc[
        (metadata.group == group, "google_drive_parent_name")
    ].values[0]
    target_path = Path(PROCESSED_DATA_PATH, "sepsis", folder_name)
    return list(target_path.glob(f"**/*{cell_type}*.npy"))


def get_healthy_patient_data(patient_id, cell_type, metadata):
    group = f"Healthy#{patient_id}"
    folder_name = metadata.loc[
        (metadata.group == group, "google_drive_parent_name")
    ].values[0]
    target_path = Path(PROCESSED_DATA_PATH, "igra", folder_name)
    return list(target_path.glob(f"**/*{cell_type}*.npy"))


def create_target_dataset(
    target,
    celltype,
    test_patients,
    sepsis_metadata,
    igra_metadata,
):

    map_dict = {
        "timepoint1": partial(
            get_timepoint_patient_data, timepoint=1, metadata=sepsis_metadata
        ),
        "timepoint2": partial(
            get_timepoint_patient_data, timepoint=2, metadata=sepsis_metadata
        ),
        "timepoint3": partial(
            get_timepoint_patient_data, timepoint=3, metadata=sepsis_metadata
        ),
        "healthy": partial(get_healthy_patient_data, metadata=igra_metadata),
    }
    patient_dict = {
        "timepoint1": SEPSIS_PATIENTS,
        "timepoint2": SEPSIS_PATIENTS,
        "timepoint3": SEPSIS_PATIENTS,
        "healthy": HEALTHY_PATIENTS,
    }
    target_input_data_path_list = []
    target_test_data_path_list = []

    target_func = partial(map_dict[target], cell_type=celltype)
    target_total_patients = patient_dict[target]
    target_input_patients = target_total_patients - set(test_patients)

    for p in target_input_patients:
        target_input_data_path_list.extend(target_func(patient_id=p))
    for p in test_patients:
        target_test_data_path_list.extend(target_func(patient_id=p))

    return target_input_data_path_list, target_test_data_path_list


def create_task_dataset(
    target1,
    target2,
    celltype,
    target1_test,
    target2_test,
    sepsis_metadata,
    igra_metadata,
):
    (
        target1_input_data_path_list,
        target1_test_data_path_list,
    ) = create_target_dataset(
        target1, celltype, target1_test, sepsis_metadata, igra_metadata
    )
    (
        target2_input_data_path_list,
        target2_test_data_path_list,
    ) = create_target_dataset(
        target2, celltype, target2_test, sepsis_metadata, igra_metadata
    )
    return (
        target1_input_data_path_list,
        target1_test_data_path_list,
        target2_input_data_path_list,
        target2_test_data_path_list,
    )


def split_train_valid_test(arr):
    np.random.shuffle(arr)

    train_idx = arr[: int(len(arr) * 0.8)]
    valid_idx = arr[int(len(arr) * 0.8) : int(len(arr) * 0.9)]
    test_idx = arr[int(len(arr) * 0.9) :]
    return train_idx, valid_idx, test_idx


def run_task(task, parameters, sepsis_metadata, igra_metadata):
    (
        target1_input_data_path_list,
        target1_test_data_path_list,
        target2_input_data_path_list,
        target2_test_data_path_list,
    ) = create_task_dataset(
        parameters["group1"],
        parameters["group2"],
        parameters["celltype"],
        parameters["group1_test"],
        parameters["group2_test"],
        sepsis_metadata,
        igra_metadata,
    )

    input_X = np.array(
        target1_input_data_path_list + target2_input_data_path_list
    )
    input_Y = np.array(
        [0] * len(target1_input_data_path_list)
        + [1] * len(target2_input_data_path_list)
    )
    input_idx = np.arange(len(input_X))
    train_idx, valid_idx, test_idx = split_train_valid_test(input_idx)

    results = {
        "train_X": input_X[train_idx],
        "train_Y": input_Y[train_idx],
        "valid_X": input_X[valid_idx],
        "valid_Y": input_Y[valid_idx],
        "test_X": input_X[test_idx],
        "test_Y": input_Y[test_idx],
        "test_one_X": np.array(
            target1_test_data_path_list + target2_test_data_path_list
        ),
        "test_one_Y": np.array(
            [0] * len(target1_test_data_path_list)
            + [1] * len(target2_test_data_path_list)
        ),
        "label": {0: parameters["group1"], 1: parameters["group2"]},
    }

    with open(
        f"task/{task}_{parameters['group1']}_{parameters['group2']}_{parameters['celltype']}.pkl",
        "wb",
    ) as f:
        pickle.dump(results, f)

    return results


def main():
    engine = get_engine(HOST, PORT, USER, PASSWORD, DBNAME)
    sepsis_metadata = pd.read_sql(
        "SELECT * FROM 2022_tomocube_sepsis_patient", engine
    )[["patient_id", "group", "google_drive_parent_name"]]
    igra_metadata = pd.read_sql(
        "SELECT * FROM 2022_tomocube_igra_patient", engine
    )[["patient_id", "group", "google_drive_parent_name"]]

    with open("task/task.yaml", "r") as f:
        task_yaml = yaml.load(f, Loader=yaml.FullLoader)

    for task, parameters in task_yaml.items():
        print(run_task(task, parameters, sepsis_metadata, igra_metadata))


if __name__ == "__main__":
    main()
