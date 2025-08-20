def generate_blind_docking_notebook_str(ligand_name: str):
    # read jupyter notebook template file as text
    with open('./api/business/docking/BlindDock_template.ipynb', 'r') as file:
        content = file.read()
    # replace PDB_INPUT with the actual PDB
    PDB_INPUT = f'{ligand_name}'
    content = content.replace('{PDB_INPUT}', PDB_INPUT)
    return content

def generate_blind_docking_notebook(ligand_name: str):
    content = generate_blind_docking_notebook_str(ligand_name)
    with open(f'BlindDock_{ligand_name}.ipynb', 'w') as file:
        file.write(content)
    # check if notebook works afterwards

