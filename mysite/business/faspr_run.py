from mysite.business.alderaan import Alderaan
import os

class FasprRun:
    alderaan = None
    alderaan_pharmaco_folder = os.path.join('/', 'home', 'reedsc')
    scratch_folder = os.path.join('website_activity')
    alderaan_scratch_folder = os.path.join('/','storage','chemistry','projects','pharmacogenomics')
    alderaan_alpha_folder = os.path.join(alderaan_scratch_folder, 'alphafold')
    alpha_folder = os.path.join('Documents','alphafold')
    temp_folder = os.path.join(scratch_folder, 'tmp')

    def __init__(self):
        self.alderaan = Alderaan()
        self.FASPR_pdb_text = self.run_FASPR()
        # print(self.FASPR_pdb_text)

    def run_FASPR(self):
        FASPR_command = f"FASPR/FASPR -i {self.temp_folder}/pdb_temporary.txt -o {self.temp_folder}/FASPR_output.pdb -s {self.temp_folder}/repacked_pdb.txt"
        FASPR_out, success = self.alderaan.run_command(FASPR_command)
        # print(FASPR_out)
        cat_command = f"cat {self.temp_folder}/FASPR_output.pdb | tee FASPR_output.txt"
        FASPR_pdb_text, success = self.alderaan.run_command(cat_command)
        # print(success, FASPR_pdb_text)
        with open('FASPR_output.txt', 'w+') as f:
            f.write(FASPR_pdb_text)
        return FASPR_pdb_text
