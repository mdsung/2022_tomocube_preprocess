import os
import pandas as pd

os.environ["PYTHONPATH"] = "."

rule create_metadata_table:
    input:  
        script = "src/create_tomocube_metadata.py"
    output:
        "data/processed/tomocube_meta.csv",
    shell:
        "python {input.script}"

rule create_target_file_table:
    input:
        "data/processed/tomocube_meta.csv",
        script = "src/create_target_file_list.py"
    output:
        "data/processed/target_files.txt"
    shell:
        "python {input.script}"

rule tiff_to_numpy:
    input:
        script = "src/tiff_to_numpy.py",
        tiff = "{datapath}/raw/{sample}.tiff",
    output:
        "{datapath}/processed/raw_numpy/{sample}.npy"
    shell:
        "python {input.script} '{input.tiff}'"

rule raw_to_input:
    input:
        script = "src/raw_numpy_to_input.py",
        raw = "{datapath}/raw_numpy/{sample}.npy",
    output:
        "{datapath}/input/{sample}.npy"
    params:
        size_x = 64,
        size_y = 64,
        size_z = 64
    shell:
        "python {input.script} '{input.raw}' {params.size_x} {params.size_y} {params.size_z}"

rule inputs:
    input:
        "data/processed/target_files.txt",
        expand("{target}", target = open('data/processed/target_files.txt', 'r').read().splitlines())
