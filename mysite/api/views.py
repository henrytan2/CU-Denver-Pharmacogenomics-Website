from rest_framework.views import APIView
from rest_framework.response import Response
from mysite.business.faspr_prep import FasprPrep

class FasprPrepAPI(APIView):
    def post(self, request):
        ccid = request.data['CCID']
        gidd = request.data['GIDD']
        faspr_prep = FasprPrep(ccid, gidd)
        return Response(True)