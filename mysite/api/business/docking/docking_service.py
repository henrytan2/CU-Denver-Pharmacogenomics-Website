import io, zipfile
from pathlib import Path
from zipfile import ZIP_DEFLATED
from .Blind_Docking_notebook_generator import generate_blind_docking_notebook_str
from .Molecular_Docking_notebook_generator import generate_molecular_docking_notebook_str
from .AF_Docking_notebook_generator import generate_af_molecular_docking_notebook_str, generate_blind_docking_notebook_alphafold_str
from ..alderaan import Alderaan


def generate_docking_zip_output(ligand_name: str):
    buf = io.BytesIO()

    # Prefer absolute path to avoid CWD surprises
    src = Path("./api/business/docking/docking_output").resolve()
    if not src.is_dir():
        raise ValueError(f"{src} is not a directory")

    output_dir = f"docking_output_{ligand_name}"
    blind_docking_notebook = generate_blind_docking_notebook_str(ligand_name)
    molecular_docking_notebook = generate_molecular_docking_notebook_str(ligand_name)

    with zipfile.ZipFile(buf, "w", compression=ZIP_DEFLATED) as z:
        for path in src.rglob("*"):
            if path.is_file():
                rel = path.relative_to(src)
                arcname = Path(output_dir) / rel
                z.write(path, arcname=str(arcname))

        if blind_docking_notebook is not None:
            arcname = Path(output_dir) / f'Blind_dock_{ligand_name}.ipynb'
            z.writestr(str(arcname), blind_docking_notebook)

        if molecular_docking_notebook is not None:
            arcname = Path(output_dir) / f'Molecular_dock_{ligand_name}.ipynb'
            z.writestr(str(arcname), molecular_docking_notebook)

    # Now the ZIP is closed and fully written
    size = buf.tell()
    buf.seek(0)
    return buf, size

def generate_docking_zip_output_alphafold(file_name: str):
    buf = io.BytesIO()

    src = Path("./api/business/docking/docking_output").resolve()
    if not src.is_dir():
        raise ValueError(f"{src} is not a directory")

    alderaan = Alderaan()
    alphafold_directory = '/home/boss/Documents/alphafold'

    output_dir = f"docking_output_{file_name}"
    pdb_contents = alderaan.read_file(f'{alphafold_directory}/{file_name}')
    pdb_gzip_stripped = file_name.strip(".gz")
    af_molecular_docking_notebook = generate_af_molecular_docking_notebook_str(pdb_gzip_stripped)
    af_blind_docking_notebook = generate_blind_docking_notebook_alphafold_str(pdb_gzip_stripped)


    with zipfile.ZipFile(buf, "w", compression=ZIP_DEFLATED) as z:
        for path in src.rglob("*"):
            if path.is_file():
                rel = path.relative_to(src)
                arcname = Path(output_dir) / rel
                z.write(path, arcname=str(arcname))
        if pdb_contents is not None:
            arcname = Path(output_dir) / pdb_gzip_stripped
            z.writestr(str(arcname), pdb_contents)

        if af_molecular_docking_notebook is not None:
            arcname = Path(output_dir) / f'Alphafold_molecular_dock_{pdb_gzip_stripped}.ipynb'
            z.writestr(str(arcname), af_molecular_docking_notebook)

        if af_blind_docking_notebook is not None:
            arcname = Path(output_dir) / f'Alphafold_blind_dock_{pdb_gzip_stripped}.ipynb'
            z.writestr(str(arcname), af_blind_docking_notebook)

    # Now the ZIP is closed and fully written
    size = buf.tell()
    buf.seek(0)
    return buf, size