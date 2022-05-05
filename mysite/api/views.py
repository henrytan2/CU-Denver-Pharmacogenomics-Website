from rest_framework.views import APIView
from rest_framework.response import Response
from mysite.business.faspr_prep import FasprPrep

class FasprPrepAPI(APIView):
    def post(self, request):
        ccid = request.data['CCID']
        gene_ID = request.data['gene_ID']
        neighbors = request.data['neighbors']
        faspr_prep = FasprPrep(ccid, gene_ID, neighbors)
        return Response(True)