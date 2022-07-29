from rest_framework.views import APIView
from rest_framework.response import Response
from mysite.business.faspr_prep import FasprPrep
from mysite.business.metabolite_gen import MetabPrep
import json
from mysite.business import plotly_trial # keep both
from mysite.business import plotly_trial # keep both

from django.core.cache import cache
from business.CCID_cache import set_CCID
from django.http import HttpResponse

class CacheCCIDAPI(APIView):
    def post(self, request):
        ccid = request.data['CCID']
        cache.set('CCID', ccid)
        success = set_CCID(ccid)
        print('success is', success)
        return HttpResponse('CCID') # works but ???

    def get(self, request):
        # ccid = request.data['CCID']
        returned_CCID = cache.get('CCID')
        print(returned_CCID, 'is returned CCID')
        return Response(returned_CCID)

    def retrieve():
        returned_CCID = cache.get('CCID')
        return returned_CCID

class FasprPrepAPI(APIView):
    def post(self, request):
        ccid = request.data['CCID']
        gene_ID = request.data['gene_ID']
        neighbors = request.data['neighbors']
        FasprPrep(ccid, gene_ID, neighbors)
        return Response(True)


    def get(self, request):
        with open('FASPR_output.txt', 'r') as f:
            ss=f.read()
            pdb_json = json.dumps(ss)
        return Response(pdb_json)


class MetabPrepAPI(APIView):
    def post(self, request):
        smiles_code = request.data['smiles']
        MetabPrep(smiles_code)
        return Response(True)