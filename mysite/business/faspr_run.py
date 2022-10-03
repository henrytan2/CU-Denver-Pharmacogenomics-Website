from mysite.business.alderaan import Alderaan
import os
import hashlib
from django.core.cache import cache


class FasprRun:
    alderaan = None
    scratch_folder = os.path.join('website_activity')
    temp_folder = os.path.join(scratch_folder, 'tmp')

    def __init__(self):
        self.alderaan = Alderaan()
        self.FASPR_pdb_text = self.run_FASPR()

    def run_FASPR(self):

        try:
            FASPR_command = f"FASPR/FASPR -i {self.temp_folder}/pdb_temporary.txt -o {self.temp_folder}/FASPR_output.pdb -s {self.temp_folder}/repacked_pdb.txt"
            FASPR_out, success = self.alderaan.run_command(FASPR_command)
            if "error!" in FASPR_out:
                print(FASPR_out)
                FASPR_pdb_text = 'Error'

            else:
                cat_command = f"cat {self.temp_folder}/FASPR_output.pdb" #| tee FASPR_output.txt
                FASPR_pdb_text, success = self.alderaan.run_command(cat_command)
                hasher = hashlib.sha1()
                protein_structure = FASPR_pdb_text.encode('utf-8')
                cache.set('protein_structure', FASPR_pdb_text)
                hasher.update(protein_structure)
                hashed_pdb = hasher.hexdigest()
                cache.set('hashed_pdb', hashed_pdb)

        except:
            FASPR_pdb_text = 'ERROR'

        return FASPR_pdb_text