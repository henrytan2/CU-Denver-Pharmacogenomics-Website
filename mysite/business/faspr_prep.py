import pickle5 as pickle
from mysite.business.alderaan import Alderaan
from Bio import SeqUtils
from Bio.PDB import Selection
from Bio.PDB import PPBuilder, NeighborSearch
from Bio.PDB.PDBParser import PDBParser
import os
import re

class FasprPrep:
    P_num = ''
    mutation_position = 0
    CCID = ''
    gene_ID = ''
    sur_aa_low = ''
    sur_aa_high = ''
    unmutated_seq = ''
    mutatseq = ''
    single_nucleotide = ''
    single_nucleotide_variation = ''
    mutated_protein_code = ''
    alderaan = None
    angstroms = 0
    positions = [0]
    # base_pharmaco_folder = os.path.join('/')
    alderaan_pharmaco_folder = os.path.join('/', 'home', 'reedsc')
    scratch_folder = os.path.join('website_activity')
    alderaan_scratch_folder = os.path.join('/','storage','chemistry','projects','pharmacogenomics')
    alderaan_alpha_folder = os.path.join(alderaan_scratch_folder, 'alphafold')
    alpha_folder = os.path.join('Documents','alphafold')
    temp_folder = os.path.join(scratch_folder, 'tmp')
    singularity_folder = os.path.join('..','..','..','storage','singularity')
    FASPR_folder = os.path.join('FASPR')

    def __init__(self, CCID, gene_ID, angstroms):
        self.alderaan = Alderaan()
        self.CCID = CCID
        self.gene_ID = gene_ID
        self.angstroms = int(angstroms)
        self.get_Pnum()
        self.unmutated_seq, self.structure, self.sequence_length = self.get_sequence_unmut()
        self.mut_pos, self.single_nucleotide, self.single_nucleotide_variation = self.get_mutation_position(CCID)
        self.unmutated_sequence = str(self.unmutated_seq)
        self.mutated_sequence = self.unmutated_sequence[:self.mutation_position - 1] + \
                                self.unmutated_sequence[self.mutation_position - \
                                1:self.mutation_position].replace(self.single_nucleotide,
                                self.single_nucleotide_variation) + self.unmutated_sequence[self.mutation_position:]
        self.positions = self.get_mutated_sequence3d(self.structure, self.mut_pos, 'A', self.angstroms) #DROP A
        self.get_mut_seq = self.capitalize(self.mutated_sequence, self.positions)
        self.mutatseq = self.make_mutatedseq_file(self.get_mut_seq)
        self.output, self.sequence_length = self.get_specific_mutation(self.unmutated_seq, self.mut_pos, self.single_nucleotide, self.positions, self. sequence_length)
        print('positions mutated will be: ', self.output)
        print('sequence length is: ', self.sequence_length)


    def get_Pnum(self):
        with open('../pharmacogenomics_website/resources/ENSG_PN_dictALL.pickle', 'rb') as f:
            ENSG_Pnum_dict = pickle.load(f)
            self.P_num = ENSG_Pnum_dict[f'{self.gene_ID}']
            print('Pnum is: ',self.P_num)

    def get_sequence_unmut(self):
        p = PDBParser()
        protein_count_command = f'ls -dq {self.alpha_folder}/AF-{self.P_num}-F*-model_v* | wc -l'
        protein_count, success = self.alderaan.run_command(protein_count_command)
        if success:
            protein_number = int(protein_count)
            if protein_number == 2:
                protein_filename = f"find '{self.alpha_folder}' -maxdepth 1 -name 'AF-{self.P_num}-F*-model_v*.pdb.gz'"
                pdb_file, success = self.alderaan.run_command(protein_filename)
                _ , self.protein_short_name = os.path.split(pdb_file[:-4])
                mkdir_command = f'mkdir {self.temp_folder}/{self.protein_short_name[:-4]}'
                self.alderaan.run_command(mkdir_command)
                gunzip_command = f'gunzip -c {pdb_file[:-1]} > {self.temp_folder}/{self.protein_short_name[:-4]}/{self.protein_short_name}'
                self.alderaan.run_command(gunzip_command)
                open_command = f"cat {self.temp_folder}/{self.protein_short_name[:-4]}/{self.protein_short_name} | tee {self.temp_folder}/pdb_temporary.txt"
                pdb_text, success = self.alderaan.run_command(open_command)
                with open('pdb_temporary.txt', 'w+') as f:
                    f.write(pdb_text)
                p = PDBParser(PERMISSIVE=1)
                structure = p.get_structure(id = '_', file = 'pdb_temporary.txt')

                ppb = PPBuilder()
                peptides = ppb.build_peptides(structure)
                PDB_sequence = peptides[0].get_sequence()
                print(PDB_sequence) #send to js?
                unmutated_sequence = PDB_sequence.lower()
                sequence_length = len(unmutated_sequence)
                return unmutated_sequence, structure, sequence_length
            else:
                print('protein in multiple files. Skipped.')

    def get_mutation_position(self, poss_mutation):
        if poss_mutation.startswith('p.') \
                and poss_mutation[2:5] != poss_mutation[-3:] \
                and poss_mutation[-3:] != 'del' \
                and poss_mutation[-3:] != 'Ter' and poss_mutation[-3:] != 'dup' \
                and len(poss_mutation) < 12:
            act_mutation = poss_mutation.split(' ')
            for mutation in act_mutation:
                # mutation_position = int(mutation[5:-3])
                mutant_n = str(re.findall(r'\d+', mutation))
                mutation_str = mutant_n.strip("['']")
                mutation_position = int(mutation_str)
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
        positions = sorted(res.id[1] for res in nearby_residues)
        print('repacked residues are', positions)
        return positions

    def capitalize(self, mutatedsequence, positions):
        split_mutatedsequence = list(mutatedsequence)
        for int in positions:
            try:
                split_mutatedsequence[int] = split_mutatedsequence[int].upper()
            except IndexError:
                print('Index out of range : ', int)
        return "".join(split_mutatedsequence)

    def make_mutatedseq_file(self, mutatseq):
        mutatseq_pipe = str(f'"{mutatseq}"')
        mutatseq_pipe += f' | tee {self.temp_folder}/repacked_pdb.txt'
        echo_command = f'echo {mutatseq_pipe}'
        save_output, success = self.alderaan.run_command(echo_command)
        chmod_command = f'{self.temp_folder}/repacked_pdb.txt'
        self.alderaan.send_chmod(chmod_command)
        return mutatseq
        # print('saved this:', mutatseq_pipe, success)

    def get_specific_mutation(self, unmutated_seq, position_mutation, single_nucleotide, positions, sequence_length):
        mutated_protein_code = unmutated_seq
        if self.unmutated_seq[position_mutation - 1] == f'{single_nucleotide}':
            mutated_protein_code = self.get_mutated_sequence3d(self.structure, self.mut_pos, 'A', self.angstroms)
            self.make_mutatedseq_file(mutated_protein_code)
        return positions, sequence_length

