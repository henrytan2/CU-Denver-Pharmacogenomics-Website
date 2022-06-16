import pickle5 as pickle
from mysite.business.alderaan import Alderaan
from Bio import SeqUtils
from Bio.PDB import PPBuilder
from Bio.PDB.PDBParser import PDBParser
import os

class FasprPrep:
    P_num = ''
    mutation_position = 0
    CCID = ''
    gene_ID = ''
    unzip_target_pdb_file = 'pdb_tmp.txt'
    sur_aa_low = ''
    sur_aa_high = ''
    unmutated_seq = ''
    single_nucleotide = ''
    single_nucleotide_variation = ''
    mutated_protein_code = ''
    alderaan = None
    neighbors = 7
    scratch_folder = os.path.join('/','storage','chemistry','projects','pharmacogenomics')
    alpha_folder = os.path.join(scratch_folder, 'alphafold')
    temp_folder = os.path.join(scratch_folder, 'tmp')
    singularity_folder = os.path.join('..','..','..','storage','singularity')
    FASPR_folder = os.path.join('/','home','reedsc','FASPR')

    def __init__(self, CCID, gene_ID, neighbors):
        self.alderaan = Alderaan()
        self.CCID = CCID
        self.gene_ID = gene_ID
        self.neighbors = int(neighbors)
        self.get_Pnum()
        self.unmutated_seq = self.get_sequence_unmut()
        self.mut_pos = self.get_mutation_position(CCID)
        self.get_mut_seq = self.get_mutated_sequence(self.unmutated_seq)
        self.make_mutatedseq_file(self.get_mut_seq)
        self.get_specific_mutation()

    def get_Pnum(self):
        with open('../pharmacogenomics_website/resources/ENSG_PN_dictALL.pickle', 'rb') as f:
            ENSG_Pnum_dict = pickle.load(f)
            self.P_num = ENSG_Pnum_dict[f'{self.gene_ID}']

    def get_sequence_unmut(self):
        p = PDBParser()
        protein_count_command = f'ls -dq {self.alpha_folder}/AF-{self.P_num}-F*-model_v* | wc -l'
        protein_count, success = self.alderaan.run_command(protein_count_command)
        if success:
            protein_number = int(protein_count)
            if protein_number == 2:
                protein_filename = f"find '{self.alpha_folder}' -maxdepth 1 -name 'AF-{self.P_num}-F*-model_v*.pdb.gz'"
                pdb_file, success = self.alderaan.run_command(protein_filename)
                _ , protein_short_name = os.path.split(pdb_file[:-4])
                mkdir_command = f'mkdir {self.temp_folder}/{protein_short_name[:-4]}'
                self.alderaan.run_command(mkdir_command)
                gunzip_command = f'gunzip -c {pdb_file[:-1]} > {self.temp_folder}/{protein_short_name[:-4]}/{protein_short_name}'
                self.alderaan.run_command(gunzip_command)
                open_command = f"cat {self.temp_folder}/{protein_short_name[:-4]}/{protein_short_name} | tee {self.temp_folder}/pdb_tmp3.txt"
                pdb_text, success = self.alderaan.run_command(open_command)

                p = PDBParser(PERMISSIVE=1)
                structure = p.get_structure(id = '_', file = 'pdb_tmp.txt')

                ppb = PPBuilder()
                peptides = ppb.build_peptides(structure)
                print(len(peptides))
                PDB_sequence = peptides[0].get_sequence()
                print(PDB_sequence)
                unmutated_sequence = PDB_sequence.lower()
                return unmutated_sequence
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
                getVals = list([val for val in mutation if val.isnumeric()])
                mutation_position = int("".join(getVals))
                return mutation_position

    def get_mutated_sequence(self, seq):
        self.position_mutation = self.get_mutation_position(self.CCID)
        print('position_mutation',self.position_mutation)
        if self.position_mutation - self.neighbors < 1:
            self.neighbors = self.position_mutation
        possible_mutation_ext = str(self.CCID)
        position_mutation = self.get_mutation_position(possible_mutation_ext)#drop?
        self.sur_aa_low = self.unmutated_seq[position_mutation - self.neighbors:position_mutation - 1].upper()
        print('sur_aa_low',self.sur_aa_low)
        self.sur_aa_high = self.unmutated_seq[position_mutation:position_mutation + (self.neighbors-1)].upper()
        print('sur_aa_high',self.sur_aa_high)
        INV = possible_mutation_ext[2:5]
        MNV = possible_mutation_ext[-3:]
        self.single_nucleotide = SeqUtils.IUPACData.protein_letters_3to1[f'{INV}'].lower()
        print(self.single_nucleotide)
        self.single_nucleotide_variation = SeqUtils.IUPACData.protein_letters_3to1[f'{MNV}']
        print(self.single_nucleotide_variation)
        self.mutated_protein_code = self.unmutated_seq[0:position_mutation - self.neighbors] + \
                               self.sur_aa_low + \
                               self.unmutated_seq[position_mutation - 1]\
                                .replace(self.single_nucleotide,
                                self.single_nucleotide_variation) + self.sur_aa_high + \
                                self.unmutated_seq[position_mutation + (self.neighbors-1):]
        print(self.mutated_protein_code)
        if len(self.mutated_protein_code) - self.position_mutation < self.neighbors:
            self.neighbors = len(self.mutated_protein_code) - self.position_mutation # test this
        # print(len(self.mutated_protein_code))
        return self.mutated_protein_code

    def make_mutatedseq_file(self, mutatseq):
        # echo_command = f'printf {mutatseq} > repack_{self.P_num}_{self.CCID[2:]}3.txt'
        mutatseq = str(f'"{mutatseq}"')
        mutatseq += f' | tee {self.temp_folder}/missing_repack.txt'
        echo_command = f'echo {mutatseq}'
        print('echo_command is ', mutatseq)
        output, success = self.alderaan.run_command(echo_command)
        print('success',success)


    def get_specific_mutation(self):

        if self.unmutated_seq[self.position_mutation - 1] == f'{self.single_nucleotide}':
            mutated_protein_code = self.get_mutated_sequence(self.unmutated_seq)
            self.make_mutatedseq_file(mutated_protein_code)

        FASPR_command = f"FASPR/FASPR -i /{self.scratch_folder}/{self.unzip_target_pdb_file} -s /{self.scratch_folder}/repack_{self.P_num}_{self.CCID[2:]}.txt  -o /{self.scratch_folder}/test_FASPR.pdb"
        # FASPR_command = f"/FASPR/FASPR -i /{self.scratch_folder}/{self.unzip_target_pdb_file} -s /{self.scratch_folder}/repack_{self.P_num}_{self.CCID[2:]}.txt  -o /{self.scratch_folder}/proteinmutations/{self.P_num}_{self.possible_mutation_ext}_FASPR.pdb"
        print(FASPR_command)
        FASPR_out, success = self.alderaan.run_command(FASPR_command)
        print(success)
        print(FASPR_out)
        # self.alderaan.run_command(
        #     f"/FASPR/FASPR -i /{self.scratch_folder}{self.unzip_target_pdb_file} -s /{self.scratch_folder}/repack_lines/repack_{self.P_num}_{possible_mutation_ext[2:]}.txt  -o /{self.scratch_folder}/proteinmutations/{self.P_num}_{self.possible_mutation_ext}_FASPR.pdb")
