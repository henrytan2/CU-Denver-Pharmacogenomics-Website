import pickle5 as pickle
from .alderaan import Alderaan
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.ResidueDepth import get_surface
import os
import re
import io
import numpy
from mysite.gtexome.models import MutationModel


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
            else:
                self.INV = 'error'
                self.MNV = 'error'
                print(self.CCID)
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
            self.disulfide_check = self.check_disulfides(self.INV, self.pdb_text, self.mutation_position, self.chain)
            if self.INV == "Pro" or self.INV == "PRO" or self.INV == "pro":
                self.proline_check = self.get_torsion_angle(self.mut_residue, self.structure)
            else:
                self.proline_check = 'No cis proline removed'
            self.buried = self.buried_residues(self.structure, self.mutation_position, self.INV, self.MNV)
            self.recommendation = 'Alphafold structure not suitable for modeling'
            if self.charge_change == 'No swap of positively and negatively charged residues.'\
                    and self.disulfide_check == 'No disulfides disrupted.' \
                    and self.proline_check == 'No cis proline removed'\
                    and not (self.buried.startswith('Charged')) \
                    and not (self.buried.startswith('Lost')) \
                    and not (self.buried.startswith('Buried')):
                self.recommendation = 'Alphafold structure suitable for modeling'

        except Exception as e:
            print(e)
            self.plddt_snv = 'structure too large'
            self.plddt_avg = 'structure too large'
            self.charge_change = 'error checking structure'
            self.disulfide_check = 'error checking structure'
            self.proline_check = 'error checking structure'
            self.buried = 'error checking structure'
            self.recommendation = 'Alphafold structure not suitable for modeling'

        self.geneID_CCID = self.gene_ID + self.CCID
        MutationModel.objects.update_or_create(geneID_CCID=self.geneID_CCID,
                                               plddt_snv=self.plddt_snv,
                                               charge_change=self.charge_change,
                                               disulfide_check=self.disulfide_check,
                                               proline_check=self.proline_check,
                                               buried=self.buried,
                                               recommendation=self.recommendation)


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

    def check_disulfides(self, INV, file, mutation_position, best_chain_id):
        disulfide_check = 'No disulfides disrupted.'
        if INV != "Cys":
            return disulfide_check
        for line in file.split('\n'):
            if line.startswith('SSBOND'):
                if line[1] == mutation_position or line[4] == mutation_position and line[3] == best_chain_id:
                    disulfide_check = 'Mutation disrupts disulfide.'

        return disulfide_check

    def get_torsion_angle(self, residue, structure):
        proline_check = 'No cis proline removed.'
        structure.atom_to_internal_coordinates()
        ric = residue.internal_coord
        torsion_angle = ric.get_angle("omg")
        torsion_abs = round(abs(torsion_angle))

        if torsion_abs not in range(150, 190):
            proline_check = 'cis proline removed.'

        return proline_check

    def charge_check(self, INV, MNV):
        charge_change = 'No swap of positively and negatively charged residues.'

        if INV == "Asp" or INV == "Glu":
            if MNV == "Lys" or MNV == "Arg" or MNV == "His":
                charge_change = "Charge switched from - to +"

        if INV == "Lys" or INV == "Arg" or INV == "His":
            if MNV == "Asp" or MNV == "Glu":
                charge_change = "Charge switched from + to -"

        return charge_change

    def buried_residues(self, structure, mut_residue, INV, MNV):

        if INV == "Gly":
            buried = "Buried Glycine replaced.  "

        elif INV == "Lys" or INV == "Arg" or INV == "His":
            if MNV == "Asp" or MNV == "Glu":
                buried = "Charge that is buried switched from + to -.  "
            elif MNV != "Lys" and MNV != "Arg" and MNV != "His":
                buried = "Lost buried positive charge.  "
            else:
                buried = "No loss of buried charges or glycine.  "

        elif INV == "Asp" or INV == "Glu":
            if MNV == "Lys" or MNV == "Arg" or MNV == "His":
                buried = "Charge that is buried switched from - to +.  "
            elif MNV != "Asp" and MNV != "Glu":
                buried = "Lost buried negative charge.  "
            else:
                buried = "No loss of buried charges or glycine.  "

        else:
            buried = "No loss of buried charges or glycine.  "

        if MNV == "Pro":
            buried += "Buried Proline introduced.  "
        else:
            buried += "No buried Proline introduced.  "

        if MNV == "Ser" or MNV == "Thr" or MNV == "Cys" or MNV == "Tyr" or MNV == "Asn" or MNV == "Gln":
            if INV != "Ser" and INV != "Thr" and INV != "Cys" and INV != "Tyr" and INV != "Asn" and INV != "Gln":
                buried += "Buried hydrophilic residue introduced.  "
            else:
                buried += "No buried charge or hydrophilic residue introduced.  "

        elif MNV == "Asp" or MNV == "Glu":
            if INV != "Asp" and INV != "Glu":
                buried += "Buried negative charge introduced.  "
            else:
                buried += "No buried charge or hydrophilic residue  introduced.  " # repeated?

        elif MNV == "Lys" or MNV == "Arg" or MNV == "His":
            if INV == "Asp" or INV == "Glu":
                buried += "" # already covered
            elif INV != "Lys" and INV != "Arg" and INV != "His":
                buried += "Buried positive charge introduced.  "
            else:
                buried += "No buried charge or hydrophilic residue  introduced.  "

        else:
            if buried.startswith("No"):
                buried += "No gain of buried charge or hydrophilic residue.  No loss of buried charge.  "
            else:
                buried += "No gain of buried charge or hydrophilic residue.  "
            return buried

        if buried.startswith("No"):
            return buried

        model = structure[0]
        chain = model['A']
        residue = chain[mut_residue]
        if not residue.has_id("CA"):
            return None
        ca = residue["CA"]
        coord = ca.get_coord()
        try:
            surface = get_surface(model, MSMS='./msms.x86_64Darwin.2.6.1')
        except:
            surface = get_surface(model, MSMS='./msms.x86_64Linux2.2.6.1') #from https://ccsb.scripps.edu/msms/downloads/
        d = surface - coord
        d2 = numpy.sum(d * d, 1)
        min_dist = numpy.sqrt(min(d2))

        if min_dist > 4:
            return buried

        else:
            buried = "No gain of buried charge, proline, or hydrophilic residue. No loss of buried charge."
            return buried