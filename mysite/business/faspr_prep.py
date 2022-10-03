import pickle5 as pickle
from mysite.business.alderaan import Alderaan
from Bio import SeqUtils
from Bio.PDB import Selection
from Bio.PDB import PPBuilder, NeighborSearch
from Bio.PDB.PDBParser import PDBParser
import os
import re


class FasprPrep:

    scratch_folder = os.path.join('website_activity')
    alpha_folder = os.path.join('Documents', 'alphafold')
    temp_folder = os.path.join(scratch_folder, 'tmp')

    def __init__(self, CCID, gene_ID, angstroms, use_alphafold, file_location):
        self.alderaan = Alderaan()
        self.CCID = CCID
        self.mutant_n = str(re.findall(r'\d+', self.CCID))
        self.mutation_str = self.mutant_n.strip("['']")
        self.mutation_position = int(self.mutation_str)
        self.gene_ID = gene_ID
        self.get_Pnum()
        self.mut_pos, self.single_nucleotide, self.single_nucleotide_variation = self.get_mutation_position(self.CCID)
        self.use_alphafold = use_alphafold
        self.file_location = file_location

        if self.use_alphafold == 'false':
            self.unmutated_seq, self.structure, self.sequence_length = self.get_sequence_unmut()

        try: self.unmutated_seq, self.structure, self.sequence_length, self.model, self.residues = \
                self.get_sequence_unmut_AF()
        except:
            self.positions = '0'
            self.mutatseq = '0'
            self.repack_pLDDT = 'structure too large'
            self.sequence_length = '0'
            return

        self.unmutated_sequence = str(self.unmutated_seq)
        self.mutated_sequence = self.unmutated_sequence[:self.mutation_position - 1] + \
                                        self.unmutated_sequence[self.mutation_position - \
                                        1:self.mutation_position].replace(self.single_nucleotide,
                                        self.single_nucleotide_variation) + \
                                        self.unmutated_sequence[self.mutation_position:]
        self.angstroms = int(angstroms)
        self.positions = self.get_mutated_sequence3d(self.structure, self.mut_pos, 'A', self.angstroms) #DROP A
        self.get_mut_seq = self.capitalize(self.mutated_sequence, self.positions)
        self.mutatseq = self.make_mutatedseq_file(self.get_mut_seq)
        self.chain = self.model['A']
        self.mut_residue = self.chain[self.mutation_position]

        pLDDT = []
        for residue in self.residues:
            if residue.has_id("CA"):
                ca = residue["CA"]
                pLDDT_score = ca.get_bfactor()
                pLDDT.append(pLDDT_score)
        self.repack_pLDDT = sum(pLDDT) / len(pLDDT)
        self.repack_pLDDT = round(self.repack_pLDDT, 2)

    def get_Pnum(self):
        with open('../pharmacogenomics_website/resources/ENSG_PN_dictALL.pickle', 'rb') as f:
            ENSG_Pnum_dict = pickle.load(f)
            self.P_num = ENSG_Pnum_dict[f'{self.gene_ID}']

    def get_sequence_unmut(self):
        open_command = f"cat {self.file_location} | tee {self.temp_folder}/pdb_temporary.txt"
        pdb_text, success = self.alderaan.run_command(open_command)
        with open('pdb_temporary.txt', 'w+') as f:
            f.write(pdb_text)
        p = PDBParser(PERMISSIVE=1)
        structure = p.get_structure(id='_', file='pdb_temporary.txt')
        ppb = PPBuilder()
        peptides = ppb.build_peptides(structure)
        PDB_sequence = peptides[0].get_sequence()
        unmutated_sequence = PDB_sequence.lower()
        sequence_length = len(unmutated_sequence)
        return unmutated_sequence, structure, sequence_length

    def get_sequence_unmut_AF(self):
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
                unmutated_sequence = PDB_sequence.lower()
                sequence_length = len(unmutated_sequence)
                return unmutated_sequence, structure, sequence_length, model, residues

    def get_mutation_position(self, poss_mutation):
        if poss_mutation.startswith('p.') \
                and poss_mutation[2:5] != poss_mutation[-3:] \
                and poss_mutation[-3:] != 'del' \
                and poss_mutation[-3:] != 'Ter' \
                and poss_mutation[-3:] != 'dup' \
                and len(poss_mutation) < 13:
            act_mutation = poss_mutation.split(' ')
            for mutation in act_mutation:
                mutant_n = str(re.findall(r'\d+', mutation))
                mutation_str = mutant_n.strip("['']")
                INV = mutation[2:5]
                MNV = mutation[-3:]
                single_nucleotide = SeqUtils.IUPACData.protein_letters_3to1[INV].lower()
                single_nucleotide_variation = SeqUtils.IUPACData.protein_letters_3to1[MNV]

                getVals = list([val for val in mutation if val.isnumeric()])
                mutation_position = int("".join(getVals))
                return mutation_position, single_nucleotide, single_nucleotide_variation

    def get_mutated_sequence3d(self, structure, mutation_position, chain_id, angstroms):
        chain = structure[0][chain_id]
        center_residues = [chain[resi] for resi in [mutation_position]]
        center_atoms = Selection.unfold_entities(center_residues, chain_id)
        atom_list = [atom for atom in structure.get_atoms() if atom.name == 'CA']
        ns = NeighborSearch(atom_list)
        nearby_residues = {res for center_atom in center_atoms for res in ns.search(center_atom.coord, angstroms, 'R')}
        positions = sorted(int(res.id[1]) for res in nearby_residues)# int?
        return positions

    def capitalize(self, mutatedsequence, positions):
        split_mutatedsequence = list(mutatedsequence)
        for res in positions:
            res_p = int(res)
            try:
                split_mutatedsequence[res_p-1] = split_mutatedsequence[res_p-1].upper()
            except IndexError:
                print('Index out of range : ', res_p-1)
        return "".join(split_mutatedsequence)

    def make_mutatedseq_file(self, mutatseq):
        mutatseq_pipe = str(f'"{mutatseq}"')
        mutatseq_pipe += f' | tee {self.temp_folder}/repacked_pdb.txt'
        echo_command = f'echo {mutatseq_pipe}'
        save_output, success = self.alderaan.run_command(echo_command)
        chmod_command = f'{self.temp_folder}/repacked_pdb.txt'
        self.alderaan.send_chmod(chmod_command)
        return mutatseq