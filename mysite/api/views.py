from rest_framework.views import APIView
from rest_framework.response import Response
from mysite.business.faspr_prep import FasprPrep
import json

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