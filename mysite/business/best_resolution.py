import os
from mysite.business.alderaan import Alderaan

class FindBestResolution:


    def __init__(self, gene_ID):
        self.alderaan = Alderaan()
        self.best_resolution = 'false'
        self.remote_pdb_path = os.path.abspath(
            '/home/boss/website_activity/remote_pdb/remote_pdb'
        )
        self.ENSG = gene_ID
        if self.ENSG == '0':
            self.best_resolution = "add Gene ID and refresh"
            self.file_location = None
        else:
            self.best_resolution, self.file_location = self.get_best_pdb(self.ENSG)

    def get_best_pdb(self, ENSG):

        best_res = f'source {self.remote_pdb_path}/env/bin/activate; cd {self.remote_pdb_path}; python find_best_strucutre.py {ENSG}'
        returned_results, success = self.alderaan.run_command(best_res)
        returned_results = returned_results.split('\n')
        best_resolution = returned_results[0]
        file_location = returned_results[1]
        return best_resolution, file_location
