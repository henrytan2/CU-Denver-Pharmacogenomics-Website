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
from rest_framework import serializers

from django.http import HttpResponse

# class AccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         # model = Account
#         fields = ['residue']

class CacheCCIDAPI(APIView):
    def post(self, request):
        ccid = request.data['CCID']
        cache.set('CCID', ccid)
        success = set_CCID(ccid)
        print('CacheCCIDAPI post is', success, ccid)
        return HttpResponse({'foo':'bar'})

    def get(self, request):
        returned_CCID = cache.get('CCID')
        print(returned_CCID, 'is returned CCID')
        return Response(returned_CCID)

    def retrieve():
        returned_CCID = cache.get('CCID')
        return returned_CCID


class CachePositionsAPI(APIView):

    def post(self, request):
        positions = request.data['positions']
        cache.set('positions', positions)
        success = set_positions(positions)
        print('CachePositionsAPI post is', success, positions)
        return HttpResponse({'foo':'bar'})

    def get(self, request):
        returned_positions = cache.get('positions')
        print(returned_positions, 'is returned positions')
        return Response(returned_positions)



class FasprPrepAPI(APIView):

    def post(self, request):
        ccid = request.data['CCID']
        gene_ID = request.data['gene_ID']
        neighbors = request.data['neighbors']
        residues = FasprPrep(ccid, gene_ID, neighbors)
        print('residues.output is', residues.output)
        return Response({"residue_output": list(residues.output)})

    def get(self, request):
        with open('FASPR_output.txt', 'r') as f:
            ss=f.read()
            pdb_json = json.dumps(ss)
        return Response(pdb_json)


class FasprRunAPI(APIView):
    def post(self, request):
        FasprRun()
        return Response(True)


class MetabPrepAPI(APIView):
    def post(self, request):
        smiles_code = request.data['smiles']
        MetabPrep(smiles_code)
        return Response(True)