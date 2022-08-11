from rest_framework.views import APIView
from rest_framework.response import Response
from mysite.business.faspr_prep import FasprPrep
from mysite.business.faspr_run import FasprRun
from mysite.business.metabolite_gen import MetabPrep
import json
from mysite.business import plotly_trial # keep both
from mysite.business import plotly_trial # keep both

from django.core.cache import cache
from mysite.business.CCID_cache import set_CCID
from mysite.business.CCID_cache import set_positions
from mysite.business.CCID_cache import set_length
from rest_framework import serializers

from django.http import HttpResponse


class FasprPrepAPI(APIView):

    def post(self, request):
        ccid = request.data['CCID']
        gene_ID = request.data['gene_ID']
        angstroms = request.data['angstroms']
        faspr_prep = FasprPrep(ccid, gene_ID, angstroms)
        sequence_length = faspr_prep.sequence_length
        residues = faspr_prep.output
        mutatseq = faspr_prep.mutatseq
        print('residues.output is', residues)
        print('sequence_length.output is', sequence_length)
        print('mutatseq.output is', mutatseq)
        return Response({"residue_output": list(residues), "sequence_length": sequence_length, "mut_seq":mutatseq})

    def get(self, request):
        with open('FASPR_output.txt', 'r') as f:
            ss=f.read()
            pdb_json = json.dumps(ss)
        return Response(pdb_json)


class FasprRunAPI(APIView):
    def post(self, request):
        FasprRun()
        return Response(True)


class CacheCCIDAPI(APIView):
    def post(self, request):
        ccid = request.data['CCID']
        cache.set('CCID', ccid)
        success = set_CCID(ccid)
        print('CacheCCIDAPI post is', success, ccid)
        return HttpResponse({'CCID':'CCID'})

    def get(self, request):
        returned_CCID = cache.get('CCID')
        print(returned_CCID, 'is returned CCID')
        return Response(returned_CCID)


class CachePositionsAPI(APIView):
    def post(self, request):
        positions = request.data['positions[]']#[:]
        cache.set('positions', positions)
        success = set_positions(positions)
        print('CachePositionsAPI Positions post is', success, positions)
        return HttpResponse({'positions':positions})

    def get(self, request):
        returned_positions = cache.get('positions')
        print(returned_positions, 'is returned positions from CachePositionsAPI')
        return Response(returned_positions)

class CacheLengthAPI(APIView):
    def post(self, request):
        sequence_length = request.data['sequence_length']
        cache.set('sequence_length', sequence_length)
        success = set_length(sequence_length)
        print('CachePositionsAPI Length post is', success, sequence_length)
        return HttpResponse({'sequence_length':sequence_length})

    def get(self, request):
        returned_length = cache.get('sequence_length')
        print(returned_length, 'is returned sequence_length from CacheLengthAPI')
        return Response(returned_length)


class MetabPrepAPI(APIView):
    def post(self, request):
        smiles_code = request.data['smiles']
        MetabPrep(smiles_code)
        return Response(True)