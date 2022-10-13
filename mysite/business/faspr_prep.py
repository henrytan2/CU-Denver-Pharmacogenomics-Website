import pickle5 as pickle
from mysite.business.alderaan import Alderaan
from Bio import SeqUtils
from Bio.PDB import Selection
from Bio.PDB import PPBuilder, NeighborSearch
from Bio.PDB.PDBParser import PDBParser
import os
import re
import io
from django.core.cache import cache

class FasprPrep:

    scratch_folder = os.path.join('website_activity')
    alpha_folder = os.path.join('Documents', 'alphafold')
    temp_folder = os.path.join(scratch_folder, 'tmp')

    def __init__(self, CCID, gene_ID, angstroms, use_alphafold, file_location, chain_id):
        self.alderaan = Alderaan()
        self.CCID = CCID
        self.mutant_n = str(re.findall(r'\d+', self.CCID))
        self.mutation_str = self.mutant_n.strip("['']")
        self.mutation_position = int(self.mutation_str)
        self.gene_ID = gene_ID
        self.angstroms = angstroms
        self.get_Pnum()
        self.mut_pos, self.single_nucleotide, self.single_nucleotide_variation = self.get_mutation_position(self.CCID)
        self.use_alphafold = use_alphafold
        self.file_location = file_location
        self.chain_id = 'A' #= response.chain_id;'A' #get from remote_pdb

        # if self.file_location == 'empty':
        #     print('no experimental file provided, using AF')
        #     self.use_alphafold == 'true'

        if self.use_alphafold == 'false':
            try:
                self.structure, self.header = self.get_sequence_unmut(self.file_location)
                self.repack_pLDDT = 'using experimental'
                if self.chain_id == 'empty':
                    self.chain_id = 'A'
                    print('using chain A')
            except:
                self.positions = '0'
                self.mutatseq = '0'
                self.repack_pLDDT = 'exp structure not suitable'
                self.sequence_length = '0'

        else:
            try:
                self.structure, self.protein_location, self.header = self.get_sequence_unmut_AF()

            except:
                self.positions = '0'
                self.mutatseq = '0'
                self.repack_pLDDT = 'structure too large'
                self.sequence_length = '0'
                return

        try:
            self.unmutated_seq, self.sequence_length, self.model, self.residues, self.positions = \
                self.get_structure_properties(self.structure, self.mutation_position, self.angstroms, self.chain_id)

        except:
            print('using AF instead')#pass worning to html
            self.structure, self.protein_location, self.header = self.get_sequence_unmut_AF()

        self.unmutated_sequence = str(self.unmutated_seq)
        self.mutated_sequence = self.unmutated_sequence[:self.mutation_position - 1] + \
                                        self.unmutated_sequence[self.mutation_position - \
                                        1:self.mutation_position].replace(self.single_nucleotide,
                                        self.single_nucleotide_variation) + \
                                        self.unmutated_sequence[self.mutation_position:]

        if self.single_nucleotide != self.unmutated_sequence[self.mutation_position - 1:self.mutation_position]:
            print('self.single_nucleotide is', self.single_nucleotide, 'self.unmutated_sequence[self.mutation_position - 1:self.mutation_position]', self.unmutated_sequence[self.mutation_position - 1:self.mutation_position])

        self.angstroms = int(angstroms)
        # self.positions = self.get_mutated_sequence3d(self.structure, self.mut_pos, self.chain_id, self.angstroms)
        self.get_mut_seq = self.capitalize(self.mutated_sequence, self.positions)
        self.chain = self.model['A']
        self.mut_residue = self.chain[self.mutation_position]

        if self.use_alphafold != 'false':
            pLDDT = []
            for x in self.positions:
                self.repacked_residue = self.chain[x]
                if self.repacked_residue.has_id("CA"):
                    ca = self.repacked_residue["CA"]
                    pLDDT_score = ca.get_bfactor()
                    pLDDT.append(pLDDT_score)
            self.repack_pLDDT = sum(pLDDT) / len(pLDDT)
            self.repack_pLDDT = round(self.repack_pLDDT, 2)

    def get_Pnum(self):
        with open('../pharmacogenomics_website/resources/ENSG_PN_dictALL.pickle', 'rb') as f:
            ENSG_Pnum_dict = pickle.load(f)
            self.P_num = ENSG_Pnum_dict[f'{self.gene_ID}']

    def get_sequence_unmut(self, file_location):
        # open_command = f"cat {self.file_location} | tee {self.temp_folder}/pdb_temporary.txt"
        open_command = f"cat {file_location}"
        pdb_text, success = self.alderaan.run_command(open_command)
        p = PDBParser(PERMISSIVE=1)
        pdb_stream = io.StringIO(pdb_text)
        structure = p.get_structure(id='_', file=pdb_stream)
        # protein_location = self.file_location
        cache.set('native_structure', pdb_stream)

        header = []
        for line in pdb_stream:
            if not line.startswith('ATOM'):
                header.append(line)
            if line.startswith('ATOM'):
                break
        header = (''.join(header))
        structure = p.get_structure(id='_', file=pdb_stream)

        return structure, header

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
                protein_location = f"{self.temp_folder}/{self.protein_short_name[:-4]}/{self.protein_short_name}"
                open_command = f"cat {protein_location}"# | tee {self.temp_folder}/pdb_temporary.txt"
                pdb_text, success = self.alderaan.run_command(open_command)
                p = PDBParser(PERMISSIVE=1)
                pdb_stream = io.StringIO(pdb_text)

                header = []
                for line in pdb_stream:
                    if not line.startswith('ATOM'):
                        header.append(line)
                    if line.startswith('ATOM'):
                        break
                header = (''.join(header))
                structure = p.get_structure(id='_', file=pdb_stream)
                return structure, protein_location, header


    def get_structure_properties(self, structure, mutation_position, angstroms, chain_id):
        model = structure[0]
        residues = model.get_residues()
        ppb = PPBuilder()
        if len(structure) > 1:
            peptides = ppb.build_peptides(model)# multi chain experimental
            # chain = structure[chain_id]#drop [0] (use model) for multi-chain exp. Keep [0] for AF
        else:
            peptides = ppb.build_peptides(structure)#AF and single chain
            # chain = structure[0][chain_id]#drop [0] (use model) for multi-chain exp. Keep [0] for AF
        PDB_sequence = peptides[0].get_sequence()
        unmutated_sequence = PDB_sequence.lower()
        sequence_length = len(unmutated_sequence)
        # center_residues = [chain[resi] for resi in [mutation_position]]
        # center_atoms = Selection.unfold_entities(center_residues, chain_id)
        # if len(structure) > 1:
        #     atom_list = [atom for atom in structure[0].get_atoms() if atom.name == 'CA']  # drop 0?
        # else:
        #     atom_list = [atom for atom in structure[0].get_atoms() if atom.name == 'CA']  # drop 0?
        #
        chain = structure[0][chain_id]
        center_residues = [chain[resi] for resi in [mutation_position]]
        center_atoms = Selection.unfold_entities(center_residues, chain_id)
        atom_list = [atom for atom in structure.get_atoms() if atom.name == 'CA']

        ns = NeighborSearch(atom_list)
        print(ns)
        nearby_residues = {res for center_atom in center_atoms for res in ns.search(center_atom.coord, angstroms, 'R')}
        print('a')
        positions = sorted(int(res.id[1]) for res in nearby_residues)# int?
        print('a')
        return unmutated_sequence, sequence_length, model, residues, positions

    # def get_mutated_sequence3d(self, structure, mutation_position, chain_id, angstroms):
        # chain = structure[0][chain_id] #drop [0] for exp
        # center_residues = [chain[resi] for resi in [mutation_position]]
        # center_atoms = Selection.unfold_entities(center_residues, chain_id)
        # atom_list = [atom for atom in structure.get_atoms() if atom.name == 'CA']
        # ns = NeighborSearch(atom_list)
        # nearby_residues = {res for center_atom in center_atoms for res in ns.search(center_atom.coord, angstroms, 'R')}
        # positions = sorted(int(res.id[1]) for res in nearby_residues)# int?
        # return positions

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
                # mutation_str = mutant_n.strip("['']")
                inv = mutation[2:5]
                mnv = mutation[-3:]
                single_nucleotide = SeqUtils.IUPACData.protein_letters_3to1[inv].lower()
                single_nucleotide_variation = SeqUtils.IUPACData.protein_letters_3to1[mnv]

                getVals = list([val for val in mutation if val.isnumeric()])
                mutation_position = int("".join(getVals))
                return mutation_position, single_nucleotide, single_nucleotide_variation

    def capitalize(self, mutatedsequence, positions):
        split_mutatedsequence = list(mutatedsequence)
        for res in positions:
            res_p = int(res)
            try:
                split_mutatedsequence[res_p-1] = split_mutatedsequence[res_p-1].upper()
            except IndexError:
                print('Index out of range : ', res_p-1)
        return "".join(split_mutatedsequence)
