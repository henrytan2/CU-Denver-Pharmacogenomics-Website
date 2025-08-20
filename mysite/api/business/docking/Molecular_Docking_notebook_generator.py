def generate_molecular_docking_notebook_str(protein_name: str):
    # read jupyter notebook template file as text
    with open('./api/business/docking/MolecularDocking_template.ipynb', 'r') as file:
        content = file.read()
    # replace PDB_INPUT with the actual PDB
    PDB_INPUT = f'{protein_name}'
    content = content.replace('{PDB_INPUT}', PDB_INPUT)

def generate_molecular_docking_notebook(protein_name: str):
    content = generate_molecular_docking_notebook_str(protein_name)
    with open(f'8.-Test_Docking_{protein_name}.ipynb', 'w') as file:
        file.write(content)
    # check if notebook works afterwards