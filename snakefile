DATA_PATH = "/data/tomocube/raw/"

rule create_metadata_table:
    input:  
        script = "src/create_tomocube_metadata.py"
    output:
        "data/processed/tomocube_metadata.csv",
    shell:
        "python {input.script}"

checkpoint create_target_file_list:
    input:
        meta = "data/processed/tomocube_metadata.csv",
        script = "src/create_target_file_list.py"
    output:
        "data/processed/target_files.txt"
    shell:
        "python {input.script} {DATA_PATH} {input.meta}"

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
        raw = "{datapath}/processed/raw_numpy/{sample}.npy",
        meta = "data/processed/tomocube_metadata.csv"
    output:
        "{datapath}/processed/input/{sample}.npy"
    params:
        size_x = 64,
        size_y = 64,
        size_z = 64
    shell:
        "python {input.script} '{input.raw}' {input.meta} {params.size_x} {params.size_y} {params.size_z}"



def read_target_file_list(wildcards):
    with open(checkpoints.create_target_file_list.get().output[0]) as f:
        targets = [target for target in f.read().split('\n')]  # we dont want empty lines
        return expand("{target}", target=targets)

rule all:
    input:
        read_target_file_list