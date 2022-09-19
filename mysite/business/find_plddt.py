import pickle5 as pickle
from mysite.business.alderaan import Alderaan
from Bio.PDB import PPBuilder
from Bio.PDB.PDBParser import PDBParser
import os
import re

class CheckPLDDT:

    def __init__(self, gene_ID, CCID):
        self.alderaan = Alderaan()
        self.CCID = CCID
        self.mutant_n = str(re.findall(r'\d+', self.CCID))
        self.mutation_str = self.mutant_n.strip("['']")
        self.mutation_position = int(self.mutation_str)
        self.alpha_folder = os.path.join('Documents', 'alphafold')
        self.scratch_folder = os.path.join('website_activity')
        self.temp_folder = os.path.join(self.scratch_folder, 'tmp')
        self.gene_ID = gene_ID
        self.specificPnum = self.get_Pnum()
        self.AF_residues, self.model = self.get_sequence_unmut_AF(self.alpha_folder, self.get_Pnum)
        self.chain = self.model['A']
        self.mut_residue = self.chain[self.mutation_position]
        pLDDT = []
        self.plddt_snv = self.mutation_pLDDT(self.mut_residue)

        for residue in self.AF_residues:
            self.plddt_avg = self.average_pLDDT(residue, pLDDT)

    def get_Pnum(self):
        with open('../pharmacogenomics_website/resources/ENSG_PN_dictALL.pickle', 'rb') as f:
            ENSG_Pnum_dict = pickle.load(f)
            self.P_num = ENSG_Pnum_dict[f'{self.gene_ID}']
            print('Pnum is: ', self.P_num)

    def get_sequence_unmut_AF(self, alpha_folder, P_num):
        # p = PDBParser()
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
                if success == True:
                    gunzip_command = f'gunzip -c {pdb_file[:-1]} > {self.temp_folder}/{self.protein_short_name[:-4]}/{self.protein_short_name}'
                    self.alderaan.run_command(gunzip_command)
                open_command = f"cat {self.temp_folder}/{self.protein_short_name[:-4]}/{self.protein_short_name} | tee {self.temp_folder}/pdb_temporary.txt"
                pdb_text, success = self.alderaan.run_command(open_command)
                with open('pdb_temporary.txt', 'w+') as f:
                    f.write(pdb_text)
                p = PDBParser(PERMISSIVE=1)
                structure = p.get_structure(id='_', file='pdb_temporary.txt')
                model = structure[0]

                residues = model.get_residues()
                ppb = PPBuilder()
                peptides = ppb.build_peptides(structure)
                PDB_sequence = peptides[0].get_sequence()
                # unmutated_sequence = PDB_sequence.lower()

                return residues, model
            else:
                print('protein in multiple files. Skipped.')

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
