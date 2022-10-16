import os
from mysite.api.business.alderaan import Alderaan


class FindBestResolution:

    def __init__(self, gene_ID, CCID):
        self.alderaan = Alderaan()
        self.best_resolution = 'false'
        self.CCID = CCID
        self.remote_pdb_path = os.path.abspath('/home/boss/website_activity/remote_pdb/remote_pdb')
        self.ENSG = gene_ID

        if self.ENSG.startswith('ENSG'):
            self.best_resolution, self.file_location, self.chain_id = self.get_best_pdb(self.ENSG, self.CCID)

        else:
            self.best_resolution = "Go back and add valid Gene ID + CCID"
            self.file_location = None
            self.chain_id = ''

    def get_best_pdb(self, ENSG, CCID):
        try:
            #Add venv with: source {self.remote_pdb_path}/env/bin/activate; if needed
            best_res = f'cd {self.remote_pdb_path}; python find_best_strucutre.py {ENSG} {CCID}'
            returned_results, success = self.alderaan.run_command(best_res)
            split_results = returned_results.split('\n')
            self.best_resolution = split_results[1]
            self.file_location = split_results[3]
            self.chain_id = split_results[4]
            if split_results[0].startswith('best structure lacks SNV site'):
                self.best_resolution = 'best structure lacks SNV site'
            if split_results[1].startswith('best structure lacks SNV site'):
                self.best_resolution = 'best structure lacks SNV site'
            if self.best_resolution.startswith('Downloading PDB structure'):
                self.best_resolution = 'submit again'
            if self.best_resolution == 'false':
                self.best_resolution = 'no structure found'

        except:
            self.best_resolution = 'error: no structure found'
            self.file_location = 'empty'
            self.chain_id = ''

        return self.best_resolution, self.file_location, self.chain_id