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
- Normalize the array(input numpy array)
- Save the input array
- Create task - included input file paths
- Save the task - with pickle
- Dataloader 

## Dataset location
* `raw`: /data/tomocube/raw/
* `raw array`: /data/tomocube/processed/raw_numpy/
* `input array`: /data/tomocube/processed/input/

