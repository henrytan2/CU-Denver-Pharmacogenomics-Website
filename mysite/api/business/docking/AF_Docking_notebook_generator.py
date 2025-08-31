def generate_af_molecular_docking_notebook_str(file_name: str):
    # read jupyter notebook template file as text
    with open('./api/business/docking/MolecularDocking_AlphaFold_template.ipynb', 'r') as file:
        content = file.read()
    # replace PDB_INPUT with the actual PDB
    PDB_INPUT = f'{file_name}'
    content = content.replace('{PDB_INPUT}', PDB_INPUT)
    return content

def generate_blind_docking_notebook_alphafold_str(alphafold_name: str):
    # read jupyter notebook template file as text
    with open('./api/business/docking/BlindDock_AlphaFold_template.ipynb', 'r') as file:
        content = file.read()
    # replace PDB_INPUT with the actual PDB
    PDB_INPUT = f'{alphafold_name}'
    content = content.replace('{PDB_INPUT}', PDB_INPUT)
    return content

def generate_af_docking_notebook(generate_func, file_name: str):
    content = generate_func(file_name)
    with open(f'Alphafold_dock_{file_name}.ipynb', 'w') as file:
        file.write(content)