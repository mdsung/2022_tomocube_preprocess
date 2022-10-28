import os

os.environ["PYTHONPATH"] = "."

rule all:
    input:
        "/home/data/tomocube/processed/raw_numpy/sepsis/20220614/20220614.163204.097.monocyte-201_RI Tomogram.npy"

rule tiff_to_numpy:
    input:
        script = "src/tiff_to_numpy.py",
        tiff = "{datapath}/raw/{sample}.tiff",
    output:
        "{datapath}/processed/raw_numpy/{sample}.npy"
    shell:
        "python {input.script} '{input.tiff}'"
