import pickle5 as pickle
from .alderaan import Alderaan
from Bio import SeqUtils
from Bio.PDB import Selection
from Bio.PDB import PPBuilder, NeighborSearch
from Bio.PDB.PDBParser import PDBParser
import os
import re
import io
from Bio.PDB import PDBIO
import uuid


class FasprPrepUpload:
    scratch_folder = os.path.join('website_activity')
    alpha_folder = os.path.join('Documents', 'alphafold')
    temp_folder = os.path.join(scratch_folder, 'tmp')

    def __init__(self, CCID, file_location):
        self.alderaan = Alderaan()
        self.CCID = CCID
        self.mutant_n = str(re.findall(r'\d+', self.CCID))
        self.mutation_str = self.mutant_n.strip("['']")
        self.mutation_position = int(self.mutation_str)
        self.get_Pnum()
        mut_position = self.get_mutation_position(self.CCID)
        if mut_position is not None:
            self.mut_pos, self.single_nucleotide, self.single_nucleotide_variation = mut_position
        else:
            self.mut_pos = None
            self.single_nucleotide = None
            self.single_nucleotide = None
        self.protein_location = file_location

        self.pdb_content = self.extract_text_with_pdftotext(file_location)
        self.chain_id = self.find_chain_id(self.pdb_content, self.mutation_position)

        self.chain_pdb = 'empty'

        #need to save uploaded file to temp_folder/file_name
        try:
            self.chain_id = 'A' #FIX
            self.file_name = uuid.uuid4()
            self.reported_location = self.temp_folder + f'/{self.file_name}'
            self.structure, self.header, self.protein_location = self.get_sequence_unmut(
                self.protein_location)
            self.model = self.structure[0]
            self.repack_pLDDT = 'Using Uploaded PDB file'
            self.unmutated_sequence, self.sequence_length = self.get_peptide_properties(self.structure)
            self.mutated_sequence = self.unmutated_sequence[:self.mutation_position - 1] + \
                                    self.unmutated_sequence[self.mutation_position - \
                                                            1:self.mutation_position].replace(
                                        self.single_nucleotide,
                                        self.single_nucleotide_variation) + \
                                    self.unmutated_sequence[self.mutation_position:]

            self.positions = self.get_mutated_sequence3d(self.structure, self.mut_pos, self.chain_id,
                                                         self.angstroms)
            if self.chain_id == 'empty':
                self.chain_id = 'A'

            self.chain = self.model[self.chain_id]
            bio_io = PDBIO()
            bio_io.set_structure(self.chain)
            bio_io.save("chain_only.pdb")
            with open("chain_only.pdb", 'r') as f:
                self.chain_pdb = f.readlines()
        #need to delete temp file
        except:
            self.positions = '0'
            self.mutatseq = '0'
            self.repack_pLDDT = 'experimental structure not suitable'
            self.sequence_length = '0'
            self.chain = self.model[self.chain_id]

        self.positions_short = str(self.positions)
        self.chain = self.model[self.chain_id]
        self.get_mut_seq = self.capitalize(self.mutated_sequence, self.positions)

    def get_Pnum(self):
        with open('./pharmacogenomics_website/resources/ENSG_PN_dictALL.pickle', 'rb') as f:
            ENSG_Pnum_dict = pickle.load(f)
            self.P_num = ENSG_Pnum_dict[f'{self.gene_ID}']

    def get_sequence_unmut(self, protein_location):
        open_command = f"cat {protein_location} "  # | tee {self.temp_folder}/pdb_temporary.txt"
        pdb_text, success = self.alderaan.run_command(open_command)
        pdb_stream = io.StringIO(pdb_text)
        header = []
        for line in pdb_stream:
            if not line.startswith('ATOM'):
                header.append(line)
            if line.startswith('ATOM'):
                break
        header = (''.join(header))
        p = PDBParser(PERMISSIVE=1)
        structure = p.get_structure(id='_', file=pdb_stream)
        return structure, header, protein_location

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
                open_command = f"cat {protein_location}"
                pdb_text, success = self.alderaan.run_command(open_command)
                p = PDBParser(PERMISSIVE=1)
                pdb_stream = io.StringIO(pdb_text)
                structure = p.get_structure(id='_', file=pdb_stream)

                header = []
                for line in pdb_stream:
                    if not line.startswith('ATOM'):
                        header.append(line)
                    if line.startswith('ATOM'):
                        break
                header = (''.join(header))
                return structure, header, protein_location
            else:
                print('protein in multiple files. Skipped.')

    def get_peptide_properties(self, structure):
        ppb = PPBuilder()
        peptides = ppb.build_peptides(structure)
        PDB_sequence = peptides[0].get_sequence()
        unmutated_sequence = PDB_sequence.lower()
        sequence_length = len(unmutated_sequence)
        return unmutated_sequence, sequence_length

    def get_mutation_position(self, mutation):
        try:
            if mutation.startswith('p.') \
                    and mutation[2:5] != mutation[-3:] \
                    and mutation[-3:] != 'del' \
                    and mutation[-3:] != 'Ter' and mutation[-3:] != 'dup' \
                    and len(mutation) < 13:
                INV = mutation[2:5]
                MNV = mutation[-3:]
                single_nucleotide = SeqUtils.IUPACData.protein_letters_3to1[INV].lower()
                single_nucleotide_variation = SeqUtils.IUPACData.protein_letters_3to1[MNV]
                getVals = list([val for val in mutation if val.isnumeric()])
                mutation_position = int("".join(getVals))
                return mutation_position, single_nucleotide, single_nucleotide_variation
            else:
                return None
        except:
            return None

    def get_mutated_sequence3d(self, structure, mutation_position, chain_id, angstroms):
        chain = structure[0][chain_id]
        center_residues = [chain[resi] for resi in [mutation_position]]  # start exp vs AF separation
        center_atoms = Selection.unfold_entities(center_residues, chain_id)
        atom_list = [atom for atom in structure.get_atoms() if atom.name == 'CA']
        ns = NeighborSearch(atom_list)
        nearby_residues = {res for center_atom in center_atoms for res in ns.search(center_atom.coord, angstroms, 'R')}
        positions = sorted(int(res.id[1]) for res in nearby_residues)  # int?
        return positions

    def capitalize(self, mutatedsequence, positions):
        split_mutatedsequence = list(mutatedsequence)
        for res in positions:
            res_p = int(res)
            try:
                split_mutatedsequence[res_p - 1] = split_mutatedsequence[res_p - 1].upper()
            except IndexError:
                print('Index out of range : ', res_p - 1)
        return "".join(split_mutatedsequence)

    def e(pdf_path):
        output_file = pdf_path.replace(".pdf", ".txt")
        os.system(f"pdftotext {pdf_path} {output_file}")
        with open(output_file, "r") as file:
            content = file.read()
        os.remove(output_file)
        return content

    def find_chain_id(pdb_content, residue_number):
        parser = PDBParser(QUIET=True)
        from io import StringIO
        structure = parser.get_structure("structure", StringIO(pdb_content))

        for model in structure:
            for chain in model:
                for residue in chain:
                    het_flag, seq_id, ins_code = residue.id
                    if seq_id == residue_number:
                        return chain.id
        return None



class FasprPrep:
    scratch_folder = os.path.join('website_activity')
    alpha_folder = os.path.join('Documents', 'alphafold')
    temp_folder = os.path.join(scratch_folder, 'tmp')

    def __init__(self, CCID, gene_ID, angstroms, use_alphafold, file_location, chain_id, reported_location):
        self.alderaan = Alderaan()
        self.CCID = CCID
        self.mutant_n = str(re.findall(r'\d+', self.CCID))
        self.mutation_str = self.mutant_n.strip("['']")
        self.mutation_position = int(self.mutation_str)
        self.gene_ID = gene_ID
        self.get_Pnum()
        mut_position = self.get_mutation_position(self.CCID)
        if mut_position is not None:
            self.mut_pos, self.single_nucleotide, self.single_nucleotide_variation = mut_position
        else:
            self.mut_pos = None
            self.single_nucleotide = None
            self.single_nucleotide = None
        self.use_alphafold = use_alphafold
        self.protein_location = file_location
        self.chain_id = chain_id
        self.chain_pdb = 'empty'

        if self.use_alphafold == 'false':
            self.reported_location = reported_location
            try:
                self.structure, self.header, self.protein_location = self.get_sequence_unmut(
                    self.protein_location)
                self.model = self.structure[0]
                self.repack_pLDDT = 'Using Experimental'
                self.unmutated_sequence, self.sequence_length = self.get_peptide_properties(self.structure)
                self.mutated_sequence = self.unmutated_sequence[:self.mutation_position - 1] + \
                                        self.unmutated_sequence[self.mutation_position - \
                                                                1:self.mutation_position].replace(
                                            self.single_nucleotide,
                                            self.single_nucleotide_variation) + \
                                        self.unmutated_sequence[self.mutation_position:]

                self.angstroms = int(angstroms)
                self.positions = self.get_mutated_sequence3d(self.structure, self.mut_pos, self.chain_id,
                                                             self.angstroms)
                if self.chain_id == 'empty':
                    self.chain_id = 'A'

                self.chain = self.model[self.chain_id]
                bio_io = PDBIO()
                bio_io.set_structure(self.chain)
                bio_io.save("chain_only.pdb")
                with open("chain_only.pdb", 'r') as f:
                    self.chain_pdb = f.readlines()

            except:
                self.positions = '0'
                self.mutatseq = '0'
                self.repack_pLDDT = 'experimental structure not suitable'
                self.sequence_length = '0'

        else:
            self.reported_location = reported_location

            try:
                self.chain_id = 'A'
                self.structure, self.header, self.protein_location = self.get_sequence_unmut_AF()
                self.model = self.structure[0]
                self.unmutated_sequence, self.sequence_length = self.get_peptide_properties(self.structure)
                self.mutated_sequence = self.unmutated_sequence[:self.mutation_position - 1] + \
                                        self.unmutated_sequence[self.mutation_position - \
                                                                1:self.mutation_position].replace(
                                            self.single_nucleotide,
                                            self.single_nucleotide_variation) + \
                                        self.unmutated_sequence[self.mutation_position:]

                self.angstroms = int(angstroms)
                self.positions = self.get_mutated_sequence3d(self.structure, self.mut_pos, self.chain_id,
                                                             self.angstroms)
                self.chain = self.model[self.chain_id]
                bio_io = PDBIO()
                bio_io.set_structure(self.chain)
                bio_io.save("chain_only.pdb")
                with open("chain_only.pdb", 'r') as f:
                    self.chain_pdb = f.readlines()

            except:
                self.positions = '0'
                self.mutatseq = '0'
                self.repack_pLDDT = 'structure too large'
                self.sequence_length = '0'
                self.get_mut_seq = ''
                self.header = ''
                return

        self.positions_short = str(self.positions)

        self.chain = self.model[self.chain_id]
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
        self.get_mut_seq = self.capitalize(self.mutated_sequence, self.positions)

    def get_Pnum(self):
        try:
            with open('./pharmacogenomics_website/resources/ENSG_PN_dictALL.pickle', 'rb') as f:
                ENSG_Pnum_dict = pickle.load(f)
                self.P_num = ENSG_Pnum_dict[f'{self.gene_ID}']
        except:
            self.P_num = None

    def get_sequence_unmut(self, protein_location):
        open_command = f"cat {protein_location} "  # | tee {self.temp_folder}/pdb_temporary.txt"
        pdb_text, success = self.alderaan.run_command(open_command)
        pdb_stream = io.StringIO(pdb_text)
        header = []
        for line in pdb_stream:
            if not line.startswith('ATOM'):
                header.append(line)
            if line.startswith('ATOM'):
                break
        header = (''.join(header))
        p = PDBParser(PERMISSIVE=1)
        structure = p.get_structure(id='_', file=pdb_stream)
        return structure, header, protein_location

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
                open_command = f"cat {protein_location}"
                pdb_text, success = self.alderaan.run_command(open_command)
                p = PDBParser(PERMISSIVE=1)
                pdb_stream = io.StringIO(pdb_text)
                structure = p.get_structure(id='_', file=pdb_stream)

                header = []
                for line in pdb_stream:
                    if not line.startswith('ATOM'):
                        header.append(line)
                    if line.startswith('ATOM'):
                        break
                header = (''.join(header))
                return structure, header, protein_location
            else:
                print('protein in multiple files. Skipped.')

    def get_peptide_properties(self, structure):
        ppb = PPBuilder()
        peptides = ppb.build_peptides(structure)
        PDB_sequence = peptides[0].get_sequence()
        unmutated_sequence = PDB_sequence.lower()
        sequence_length = len(unmutated_sequence)
        return unmutated_sequence, sequence_length

    def get_mutation_position(self, mutation):
        try:
            if mutation.startswith('p.') \
                    and mutation[2:5] != mutation[-3:] \
                    and mutation[-3:] != 'del' \
                    and mutation[-3:] != 'Ter' and mutation[-3:] != 'dup' \
                    and len(mutation) < 13:
                INV = mutation[2:5]
                MNV = mutation[-3:]
                single_nucleotide = SeqUtils.IUPACData.protein_letters_3to1[INV].lower()
                single_nucleotide_variation = SeqUtils.IUPACData.protein_letters_3to1[MNV]
                getVals = list([val for val in mutation if val.isnumeric()])
                mutation_position = int("".join(getVals))
                return mutation_position, single_nucleotide, single_nucleotide_variation
            else:
                return None
        except:
            return None

    def get_mutated_sequence3d(self, structure, mutation_position, chain_id, angstroms):
        chain = structure[0][chain_id]
        center_residues = [chain[resi] for resi in [mutation_position]]  # start exp vs AF separation
        center_atoms = Selection.unfold_entities(center_residues, chain_id)
        atom_list = [atom for atom in structure.get_atoms() if atom.name == 'CA']
        ns = NeighborSearch(atom_list)
        nearby_residues = {res for center_atom in center_atoms for res in ns.search(center_atom.coord, angstroms, 'R')}
        positions = sorted(int(res.id[1]) for res in nearby_residues)  # int?
        return positions

    def capitalize(self, mutatedsequence, positions):
        split_mutatedsequence = list(mutatedsequence)
        for res in positions:
            res_p = int(res)
            try:
                split_mutatedsequence[res_p - 1] = split_mutatedsequence[res_p - 1].upper()
            except IndexError:
                print('Index out of range : ', res_p - 1)
        return "".join(split_mutatedsequence)
