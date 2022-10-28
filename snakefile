import os
import pandas as pd

os.environ["PYTHONPATH"] = "."


rule create_target_file_table:
    input:
        "data/processed/sepsis_meta.csv",
        script = "src/create_target_file_list.py"
    output:
        "data/processed/target_files.txt"
    shell:
        "python {input.script}"

target_file_list = open('data/processed/target_files.txt', 'r').read().splitlines()

rule all:
    input:
        expand("{target}", target = target_file_list)

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
