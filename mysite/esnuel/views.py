from django.forms import model_to_dict
from django.shortcuts import render
from jupyter_lsp.specs import json
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ESNUELOutput


# Create your views here.
class EsnuelOutputInsertView(APIView):
    permission_classes = (AllowAny,)
    model = ESNUELOutput

    def post(self, request, **kwargs):
        smiles_string = request.data['smiles_string']
        elec_names = request.data['elec_names']
        elec_sites = request.data['elec_sites']
        MAAs = request.data['MAAs']
        nuc_names = request.data['nuc_names']
        nuc_sites = request.data['nuc_sites']
        MCAs = request.data['MCAs']

        self.model.objects.create(
            smiles_string=smiles_string,
            elec_names=elec_names,
            MAAs=MAAs,
            elec_sites=elec_sites,
            nuc_names=nuc_names,
            nuc_sites=nuc_sites,
            MCAs=MCAs
        )

        return Response(True)

class EsnuelOutputFetchView(APIView):
    permission_classes = (AllowAny,)
    model = ESNUELOutput

    def post(self, request, **kwargs):
        smiles_string = request.data['smiles_string']
        response = False
        try:
            esnuel_output = model_to_dict(self.model.objects.get(smiles_string=smiles_string))
            return Response(esnuel_output, status=status.HTTP_200_OK)
        except:
            print("Error occured with esnuel fetch")

        return Response(response)

