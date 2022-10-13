from mysite.business.alderaan import Alderaan
import os
import hashlib
from django.core.cache import cache


class FasprRun:

    scratch_folder = os.path.join('website_activity')
    temp_folder = os.path.join(scratch_folder, 'tmp')

    def __init__(self, mutated_sequence, protein_location):
        self.alderaan = Alderaan()
        self.mutated_sequence = mutated_sequence
        self.protein_location = protein_location
        self.save_mutatedseq_file(self.mutated_sequence)
        self.FASPR_pdb_text = self.run_faspr(self.protein_location)

    def save_mutatedseq_file(self, mutated_sequence):
        mutatseq_pipe = str(f'"{mutated_sequence}"')
        mutatseq_pipe += f' | tee {self.temp_folder}/repacked_pdb.txt'
        echo_command = f'echo {mutatseq_pipe}'
        _, success = self.alderaan.run_command(echo_command)
        chmod_command = f'{self.temp_folder}/repacked_pdb.txt'
        self.alderaan.send_chmod(chmod_command)

    def run_faspr(self, protein_location):
        try:
            faspr_command = f"FASPR/FASPR -i {protein_location} -o {self.temp_folder}/FASPR_output.pdb -s {self.temp_folder}/repacked_pdb.txt"
            faspr_out, success = self.alderaan.run_command(faspr_command)
            if "error!" in faspr_out:
                print(faspr_out)
                FASPR_pdb_text = 'Error'

            else:
                cat_command = f"cat {self.temp_folder}/FASPR_output.pdb" #| tee FASPR_output.txt
                FASPR_pdb_text, success = self.alderaan.run_command(cat_command)

                header = cache.get('pdb_header')
                FASPR_pdb_text = header + FASPR_pdb_text

                cache.set('post_faspr_pdb', FASPR_pdb_text)


        except:
            FASPR_pdb_text = 'ERROR'

        return FASPR_pdb_text