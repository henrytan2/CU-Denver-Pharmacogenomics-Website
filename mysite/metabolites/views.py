from django.shortcuts import render
from django.views import generic
from .models import Metabolite


# Create your views here.
class IndexView(generic.ListView):
    model = Metabolite
    template_name = 'metabolites.html'

    def get_queryset(self):
        inchiKey = self.request.GET['inchi_key']
        response = self.model.objects.filter(metabolite_InChi=inchiKey)
        return response
