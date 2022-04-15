import pickle5 as pickle
from mysite.business.alderaan import Alderaan
from Bio import SeqUtils
from Bio.PDB import PPBuilder
from Bio.PDB.PDBParser import PDBParser
import glob
import os

class FasprPrep:
    P_num = ''
    mutation_position = 0
    CCID = ''
    GIDD = ''
    unzip_target_pdb_file = 'tmp.pdb'
    sur_aa_low = ''
    sur_aa_high = ''
    unmutated_seq = ''
    single_nucleotide = ''
    single_nucleotide_variation = ''
    mutated_protein_code = ''
    alderaan = None

    def __init__(self, CCID, GIDD):
        self.CCID = CCID
        self.GIDD = GIDD
        self.get_Pnum()
        self.unmutated_seq = self.get_sequence_unmut()
        self.alderaan = Alderaan()

    def get_Pnum(self):
        with open('../pharmacogenomics_website/resources/ENSG_PN_dictALL.pickle', 'rb') as f:
            ENSG_Pnum_dict = pickle.load(f)
            self.P_num = ENSG_Pnum_dict[f'{self.GIDD}']

    def get_sequence_unmut(self):
        p = PDBParser()
        a = self.alderaan.run_command(f"find . -name 'AF-{self.P_num}-F*-model_v1.pdb'")
        pdb_file_unmut = glob.glob(f'AF-{self.P_num}-F*-model_v1.pdb')
        pdb_string = str(pdb_file_unmut)
        pdb_file_ = pdb_string.strip('[]')
        pdb_file = pdb_file_.strip("''")
        structure = p.get_structure('PDBunzip', pdb_file)
        ppb = PPBuilder()
        for pp in ppb.build_peptides(structure):
            PDBs = str(pp.get_sequence())
            unmutated_sequence_l = PDBs.lower()
            return unmutated_sequence_l

    def get_mutation_position(self, poss_mutation):
        if poss_mutation.startswith('p.') \
                and poss_mutation[2:5] != poss_mutation[-3:] \
                and poss_mutation[-3:] != 'del' \
                and poss_mutation[-3:] != 'Ter' and poss_mutation[-3:] != 'dup' \
                and len(poss_mutation) < 12:
            act_mutation = poss_mutation.split(' ')
            for mutation in act_mutation:
                mutation_position = int(mutation[5:-3])
                return mutation_position

    def get_mutated_sequence(self, seq):
        position_mutation = self.get_mutation_position(self.CCID)
        self.mutated_protein_code = self.unmutated_seq[0:position_mutation - 7] + \
                               self.sur_aa_low + \
                               self.unmutated_seq[position_mutation - 1]\
                                   .replace(self.single_nucleotide,
                                            self.single_nucleotide_variation) + self.sur_aa_high + self.unmutated_seq[position_mutation + 6:]
        return self.mutated_protein_code

    def make_mutatedseq_file(self, mutatseq):
        mutated_seq_file = open(f"repack_{self.P_num}_{self.CCID[2:]}.txt", "w")
        mutated_seq_file.close()
        return mutated_seq_file.write(f"{self.mutated_protein_code}")

    def get_specific_mutation(self):
        poss_mutation_ext = self.CCID
        possible_mutation_ext = str(poss_mutation_ext)
        position_mutation = self.get_mutation_position(possible_mutation_ext)

        INV = possible_mutation_ext[2:5]
        MNV = possible_mutation_ext[-3:]
        self.sur_aa_low = self.unmutated_seq[position_mutation - 7:position_mutation - 1].upper()
        self.sur_aa_high = self.unmutated_seq[position_mutation:position_mutation + 6].upper()
        self.single_nucleotide = SeqUtils.IUPACData.protein_letters_3to1[f'{INV}'].lower()
        self.single_nucleotide_variation = SeqUtils.IUPACData.protein_letters_3to1[f'{MNV}']
        if self.unmutated_seq[position_mutation - 1] == f'{self.single_nucleotide}':
            mutated_protein_code = self.get_mutated_sequence(self.unmutated_seq)
            self.make_mutatedseq_file(mutated_protein_code)
        self.alderaan.run_command(
            f"/home/boss/FASPR/FASPR -i /home/blisamahmood/PDBunzip/{self.unzip_target_pdb_file} -s /home/blisamahmood/repack_lines/repack_{self.P_num}_{possible_mutation_ext[2:]}.txt  -o /home/blisamahmood/proteinmutations/{self.P_num}_{possible_mutation_ext}_FASPR.pdb")
