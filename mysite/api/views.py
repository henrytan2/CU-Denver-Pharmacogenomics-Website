from rest_framework.views import APIView
from rest_framework.response import Response
from mysite.business.faspr_prep import FasprPrep
from mysite.business.faspr_run import FasprRun
from mysite.business.metabolite_gen import MetabPrep
from mysite.business.best_resolution import FindBestResolution

import json
from mysite.business import plotly_trial # keep both
from mysite.business import plotly_trial # keep both

from django.core.cache import cache
from mysite.business.CCID_cache import set_CCID
from mysite.business.CCID_cache import set_positions
from mysite.business.CCID_cache import set_length
from mysite.business.CCID_cache import set_PDB
from rest_framework import serializers

from django.http import HttpResponse


class FasprPrepAPI(APIView):

    def post(self, request):
        ccid = request.data['CCID']
        gene_ID = request.data['gene_ID']
        angstroms = request.data['angstroms']
        faspr_prep = FasprPrep(ccid, gene_ID, angstroms)
        sequence_length = faspr_prep.sequence_length
        residues = faspr_prep.positions
        mutatseq = faspr_prep.mutatseq
        # print('residues.output is', residues)
        # print('sequence_length.output is', sequence_length)
        # print('mutatseq.output is', mutatseq)
        return Response({"residue_output": list(residues), "sequence_length": sequence_length, "mut_seq":mutatseq})

    def get(self, request):
        returned_protein_structure = cache.get('protein_structure')
            # print(returned_protein_structure, 'is returned sequence_length from CacheProteinAPI')
        return Response(returned_protein_structure)
        # with open('FASPR_output.txt', 'r') as f:
        #     ss=f.read()
        #     pdb_json = json.dumps(ss)
        # return Response(pdb_json)


class FasprRunAPI(APIView):
    def post(self, request):
        FASPR_pdb_text = FasprRun()
        # print(FASPR_pdb_text.FASPR_pdb_text)
        return Response({'protein_structure': FASPR_pdb_text.FASPR_pdb_text})


class CacheCCIDAPI(APIView):
    def post(self, request):
        ccid = request.data['CCID']
        cache.set('CCID', ccid)
        success = set_CCID(ccid)
        return Response({'CCID':ccid})

    def get(self, request):
        returned_CCID = cache.get('CCID')
        # print(returned_CCID, 'is returned CCID')
        return Response(returned_CCID)


class CachePositionsAPI(APIView):
    def post(self, request):
        positions = request.POST.getlist('positions[]')
        cache.set('positions', positions)
        success = set_positions(positions)
        # print('CachePositionsAPI Positions post is', success, positions)
        return HttpResponse(positions)

    def get(self, request):
        returned_positions = cache.get('positions')
        # print(returned_positions, 'is returned positions from CachePositionsAPI')
        return Response(returned_positions)

class CacheLengthAPI(APIView):
    def post(self, request):
        sequence_length = request.data['sequence_length']
        cache.set('sequence_length', sequence_length)
        success = set_length(sequence_length)
        # print('CachePositionsAPI Length post is', success, sequence_length)
        return HttpResponse({'sequence_length':sequence_length})

    def get(self, request):
        returned_length = cache.get('sequence_length')
        # print(returned_length, 'is returned sequence_length from CacheLengthAPI')
        return Response(returned_length)

class CacheProteinAPI(APIView):
    def post(self, request):
        protein_structure = request.data['protein_structure']
        cache.set('protein_structure', protein_structure)
        success = set_PDB(protein_structure)
        # print('CacheProteinAPI post is', success, protein_structure)
        return Response({'protein_structure':protein_structure})

    def get(self, request):
        returned_protein_structure = cache.get('protein_structure')
        # print(returned_protein_structure, 'is returned sequence_length from CacheProteinAPI')
        return Response(returned_protein_structure)

class MetabPrepAPI(APIView):
    def post(self, request):
        smiles_code = request.data['smiles']
        MetabPrep(smiles_code)
        return Response(True)

class FindResolution(APIView):
    def post(self, request):
        gene_ID = request.data['gene_ID']
        find_best_res = FindBestResolution(gene_ID)
        resolution = find_best_res.best_resolution
        return Response({'resolution':resolution})