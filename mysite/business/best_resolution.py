import os
from mysite.business.alderaan import Alderaan

class FindBestResolution:

    def __init__(self, gene_ID):
        self.alderaan = Alderaan()
        self.best_resolution = 'false'
        self.remote_pdb_path = os.path.abspath('/home/boss/website_activity/remote_pdb/remote_pdb')
        self.ENSG = gene_ID

        if self.ENSG.startswith('ENSG'):
            self.best_resolution, self.file_location = self.get_best_pdb(self.ENSG)

        else:
            self.best_resolution = "Go back and add valid Gene ID + CCID"
            self.file_location = None

    def get_best_pdb(self, ENSG):
        try:
            #Add source {self.remote_pdb_path}/env/bin/activate; if needed
            best_res = f'cd {self.remote_pdb_path}; python find_best_strucutre.py {ENSG}'
            returned_results, success = self.alderaan.run_command(best_res)
            returned_results = returned_results.split('\n')
            self.best_resolution = returned_results[0]
            self.file_location = returned_results[1]
            if self.best_resolution.startswith('Downloading PDB structure'):
                self.best_resolution = 'reload page'

            if self.best_resolution == 'false':
                self.best_resolution = 'no structure found'

        except:
            self.best_resolution = 'no structure found'
            self.file_location = 'empty'
        return self.best_resolution, self.file_location
