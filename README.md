# Tomocube data preprocessing
- Author: MinDong Sung
- Date:  2022-10-31
---
## Object
Create a data preprocessing pipeline for tomocube data.

## Process
- Load tiff and convert to numpy array
- Save raw numpy array
- Crop the array
- Normalize the array(input numpy array) - min-max normalization per image
- Save the input array
- Create task - included input file paths
- Save the task - with pickle
- Dataloader 

## Project structure
- data/
- figure/
- src/
  - create_tomocube_metadata.sql
  - create_tomocube_metadata.py: create metadata for tomocube data
  - create_image_page.py: draw a 2d multiple figure in a page
  - create_target_file_list.py: target file list for snakemake pipeline
  - database.py: database connection related files
  - dataloader.py: dataloader with task pickle file
  - 

- task/
  - task.yaml: task specificate
        ```
        task_name:
            group1: {'healthy', 'timepoint1', 'timepoint2', 'timepoint3'}
            group2: {'healthy', 'timepoint1', 'timepoint2', 'timepoint3'}
            celltype: {'CD4', 'CD8'}
            group1_test: the patient_id list for testset 
            group2_test: the patient_id list for testset 
        ```
    - *.pkl: task file for dataloader
        ```
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
        ```
- tests/: test codes
- .env
- .gitignore
- .python-version
- README.md
- poetry.lock
- pyproject.toml
- snakemake
## Dataset location
* `raw`: /data/tomocube/raw/
* `raw array`: /data/tomocube/processed/raw_numpy/
* `input array`: /data/tomocube/processed/input/

