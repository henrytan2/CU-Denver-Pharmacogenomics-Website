import os
import json
import pickle5
from collections import defaultdict
from mysite.business.sifts import SIFTS
from Bio.PDB import PDBList
from Bio.PDB import MMCIFParser
import pandas as pd


class FindBestResolution:

    def __init__(self, gene_ID):
        self.pdb_path = os.path.abspath(
            '../pharmacogenomics_website/resources/proteins'
        )
        self.sifts_path = os.path.abspath(
            '../pharmacogenomics_website/resources/sifts'
        )
        self.ENSG = gene_ID
        self.specificPnum = self.get_Pnum(self.ENSG)
        self.ENST = self.get_ENST(self.specificPnum)
        self.sifts_ensembl = os.path.abspath(
            '../pharmacogenomics_website/resources/pdb_chain_ensembl.tsv.gz'
        )
        self.sifts_uniprot = os.path.abspath(
            '../pharmacogenomics_website/resources/pdb_chain_uniprot.tsv.gz'
        )
        self.mapping_table = self._create_mapping_table(self.sifts_ensembl)
        self.chain_id, self.protein_file_path, self.pdb_id, self.best_resolution = self.enst_to_pdb(self.ENST)

        # self.best_pdb = os.path.join(self.protein_file_path, f"{self.pdb_id}.pdb")



    def get_ENST(self, specificPnum):
        with open('../pharmacogenomics_website/resources/uniprot_to_enst.json', 'rb') as uniprot_to_enst:
            UTPdict = json.load(uniprot_to_enst)
            ENST = UTPdict[f"{specificPnum}"]
            ENST1 = ENST[0]
            return ENST1

    def get_Pnum(self, ENSG):
        with open('../pharmacogenomics_website/resources/ENSG_PN_dictALL.pickle', 'rb') as ensg_to_p_dict:
            ENSG_Pnum_dict = pickle5.load(ensg_to_p_dict)
            P_num = ENSG_Pnum_dict[f'{ENSG}']
            return P_num

    def _create_mapping_table(self, sifts_mapping_file):

        # load the mapping file into a Pandas DataFrame
        sifts_table = pd.read_csv(
            sifts_mapping_file,
            sep='\t',
            compression='gzip',
            comment='#',
            na_values='None',
            low_memory=False
        )

        sifts_table.rename(
            inplace=True,
            columns={
                'PDB': 'pdb_id',
                'CHAIN': 'pdb_chain',
                'SP_PRIMARY': 'uniprot_id',
                'GENE_ID': 'ensg_id',
                'TRANSCRIPT_ID': 'enst_id',
                'TRANSLATION_ID': 'ensp_id',
                'EXON_ID': 'exon_id'
            }
        )

        return sifts_table

    def get_resolution(self, pdb_id, pdb_path=None):
        res = 0
        pdbl = PDBList()

        if pdb_path is None:
            pdb_path = '/tmp/'
        if not os.path.exists(pdb_path):
            os.mkdir(pdb_path)

        # retrieve the PDB file for the requested PDB ID
        cif_file = os.path.join(pdb_path, pdb_id[1:3], pdb_id + '.cif')
        if not os.path.exists(cif_file) or os.stat(cif_file).st_size == 0:
            cif_file = pdbl.retrieve_pdb_file(
                pdb_id, file_format='mmCif', pdir=os.path.join(pdb_path, pdb_id[1:3])
            )

        # make a dict from meta info keys to values
        mmcif_parser = MMCIFParser(QUIET=True)
        structure_cif = mmcif_parser.get_structure(pdb_id, cif_file) #SLOW
        try:
            res = structure_cif.header['resolution']
        except KeyError:
            return None

        try:
            return float(res)
        except (ValueError, TypeError):
            return None

    def enst_to_pdb(self, enst_id, uniprot_id=None):
        protein_file_path = os.path.join(self.pdb_path)
        enst_id = enst_id.upper()
        query_str = 'enst_id == ' + '"' + enst_id + '"'

        if uniprot_id is not None:
            query_str += ' and uniprot_id == ' + '"' + uniprot_id + '"'

        # query the mapping table
        hits = self.mapping_table.query(query_str)
        # if hits.empty:

        pdb_chains = defaultdict(list)
        for _, r in hits.iterrows():
            # skip records where PDB ID or CHAIN ID is empty string
            if r['pdb_id'] and r['pdb_chain']:
                pdb_chains[r['pdb_id']].append(r['pdb_chain'])

        # remove duplicates but keep ordering
        uniq_pdb_chains = []
        for k, v in pdb_chains.items():
            uniq_pdb_chains.append((k, v[0]))

        if not uniq_pdb_chains:
            return None, None, None, None

        sifts = SIFTS(sifts_uniprot=self.sifts_uniprot, xml_dir = self.sifts_path)

        max_len = 0
        best_resolution = self.get_resolution(uniq_pdb_chains[0][0], self.pdb_path)#
        best_pdb_id = ''
        best_chain_id = ''
        for pdb_id, chain_id in uniq_pdb_chains:
            if not (pdb_id and chain_id):
                print('PDB ID is empty string for', enst_id, ', skipped')
                continue
            residue_mapping = sifts.pdb_to_uniprot(pdb_id, chain_id)
            if residue_mapping is None:
                print('Failed to obtained residue mapping from SIFTS xml file.')
                continue
            # check sequence coverage
            if max_len < len(residue_mapping):
                max_len = len(residue_mapping)
                best_pdb_id = pdb_id
                best_chain_id = chain_id
            # check resolution
            elif max_len == len(residue_mapping):
                resolution = self.get_resolution(pdb_id, self.pdb_path)
                if best_resolution is None:
                    best_resolution = resolution
                if resolution is not None and resolution < best_resolution:
                    best_pdb_id = pdb_id
                    best_chain_id = chain_id
                    best_resolution = resolution

                    protein_file_path = os.path.join(self.pdb_path, pdb_id[1:3])
                    cif_file = os.path.join(protein_file_path, f"{best_pdb_id}.cif")
                    # pymol.cmd.load(cif_file, 'myprotein')
                    # pymol.cmd.save(cif_file.replace('.cif', '.pdb'), selection='myprotein')

        # with open('best_pdb.txt', 'w+') as f:
        #     f.write(best_pdb)
        return best_chain_id, protein_file_path, best_pdb_id, best_resolution

