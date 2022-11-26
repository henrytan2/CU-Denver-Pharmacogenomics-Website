import pickle5 as pickle
from .alderaan import Alderaan
from Bio.PDB.PDBParser import PDBParser
import os
import re
import io

class CheckPLDDT:

    def __init__(self, gene_ID, CCID):
        self.alderaan = Alderaan()
        self.CCID = CCID
        try:
            self.mutant_n = str(re.findall(r'\d+', self.CCID))
            self.mutation_str = self.mutant_n.strip("['']")
            self.mutation_position = int(self.mutation_str)
            if self.CCID.startswith('p.') \
                    and self.CCID[2:5] != self.CCID[-3:] \
                    and self.CCID[-3:] != 'del' \
                    and self.CCID[-3:] != 'Ter' and self.CCID[-3:] != 'dup' \
                    and len(self.CCID) < 13:
                self.INV = self.CCID[2:5]
                self.MNV = self.CCID[-3:]
            self.alpha_folder = os.path.join('Documents', 'alphafold')
            self.scratch_folder = os.path.join('website_activity')
            self.temp_folder = os.path.join(self.scratch_folder, 'tmp')
            self.gene_ID = gene_ID
            self.specificPnum = self.get_Pnum()
            self.AF_residues, self.model, self.structure, self.pdb_text = self.get_sequence_unmut_af(self.alpha_folder, self.get_Pnum) #
            self.chain = self.model['A']
            self.mut_residue = self.chain[self.mutation_position]
            pLDDT = []
            self.plddt_snv = self.mutation_pLDDT(self.mut_residue)
            for residue in self.AF_residues:
                self.plddt_avg = self.average_pLDDT(residue, pLDDT)
            self.plddt_avg = round(self.plddt_avg, 2)
            self.charge_change = self.charge_check(self.INV, self.MNV)
            self.disulfide_check = self.check_disulfides(self.pdb_text, self.mutation_position, self.chain)
            if self.INV == "Pro" or self.INV == "Pro" or self.INV == "pro":
                self.proline_check = self.get_torsion_angle(self.mut_residue, self.structure)
            else:
                self.proline_check = 'no cis proline removed'

        except Exception as e:
            print(e)
            self.plddt_snv = 'structure too large'
            self.plddt_avg = 'structure too large'
            self.charge_change = 'error checking structure'
            self.disulfide_check = 'error checking structure'
            self.proline_check = 'error checking structure'

    def get_Pnum(self):
        with open('./pharmacogenomics_website/resources/ENSG_PN_dictALL.pickle', 'rb') as f:
            ENSG_Pnum_dict = pickle.load(f)
            self.P_num = ENSG_Pnum_dict[f'{self.gene_ID}']
            print('Pnum is: ', self.P_num)

    def get_sequence_unmut_af(self, alpha_folder, P_num):
        protein_count_command = f'ls -dq {self.alpha_folder}/AF-{self.P_num}-F*-model_v* | wc -l'
        protein_count, success = self.alderaan.run_command(protein_count_command)
        if success:
            protein_number = int(protein_count)
            if protein_number == 2:
                protein_filename = f"find '{self.alpha_folder}' -maxdepth 1 -name 'AF-{self.P_num}-F*-model_v*.pdb.gz'"
                pdb_file, success = self.alderaan.run_command(protein_filename)
                _, self.protein_short_name = os.path.split(pdb_file[:-4])
                mkdir_command = f'mkdir {self.temp_folder}/{self.protein_short_name[:-4]}'
                _, success = self.alderaan.run_command(mkdir_command)
                if success:
                    gunzip_command = f'gunzip -c {pdb_file[:-1]} > {self.temp_folder}/{self.protein_short_name[:-4]}/{self.protein_short_name}'
                    self.alderaan.run_command(gunzip_command)
                open_command = f"cat {self.temp_folder}/{self.protein_short_name[:-4]}/{self.protein_short_name}"# | tee {self.temp_folder}/pdb_temporary.txt"
                pdb_text, success = self.alderaan.run_command(open_command)
                p = PDBParser(PERMISSIVE=1)
                pdb_stream = io.StringIO(pdb_text)
                structure = p.get_structure(id='_', file=pdb_stream)
                model = structure[0]
                residues = model.get_residues()
                return residues, model, structure, pdb_text
            else:
                self.plddt_avg = 'structure too large'
                self.plddt_snv = 'structure too large'
                raise Exception('AF structure contains multiple files. Skipped')

    def average_pLDDT(self, residue, pLDDT):
        if residue.has_id("CA"):
            ca = residue["CA"]
            pLDDT_score = ca.get_bfactor()
            pLDDT.append(pLDDT_score)
            avg_plddt = sum(pLDDT) / len(pLDDT)
            return avg_plddt

    def mutation_pLDDT(self, residue):
        if residue.has_id("CA"):
            ca = residue["CA"]
            pLDDT_score = ca.get_bfactor()
            return pLDDT_score

    def charge_check(self, INV, MNV):
        charge_change = 'no change in residue charge'

        if INV == "Asp" or INV == "Glu":
            if MNV == "Lys" or MNV == "Arg" or MNV == "His":
                charge_change = "charge switched from - to +. Avoid using."
                print(charge_change)

        if INV == "Lys" or INV == "Arg" or INV == "His":
            if MNV == "Asp" or MNV == "Glu":
                charge_change = "charge switched from - to +. Avoid using."
                print(charge_change)

        return charge_change

    def check_disulfides(self, file, mutation_position, best_chain_id):
        disulfide_check = 'no disulfides disrupted'

        for line in file.split('\n'):
            if line.startswith('SSBOND'):
                if line[1] == mutation_position or line[4] == mutation_position and line[3] == best_chain_id:
                    disulfide_check = 'mutation dispruts disulfide. Avoid using.'

        return disulfide_check

    def get_torsion_angle(self, residue, structure):
        proline_check = 'no cis proline present'
        structure.atom_to_internal_coordinates()
        ric = residue.internal_coord
        torsion_angle = ric.get_angle("omg")
        torsion_abs = round(abs(torsion_angle))

        if torsion_abs not in range(150, 190):
            print(f"cis proline at mutation")
            proline_check = 'cis proline present'

        return proline_check