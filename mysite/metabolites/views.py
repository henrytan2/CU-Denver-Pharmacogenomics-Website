from django.http import HttpResponse
from django.views import generic
from .models import Metabolite
from precursor_metabolite_map.models import PrecursorMetaboliteMap
from precursors.models import Precursors
import sys
import json

# Create your views here.
class MetaboliteView(generic.ListView):
    model = Metabolite
    template_name = 'metabolite.html'
    precursor_UUIDs = []
    precursors_to_metabolites = {}

    def get_context_data(self, **kwargs):
        self.precursors_to_metabolites.clear()
        context = super(MetaboliteView, self).get_context_data(**kwargs)
        precursors = self.get_precursors()
        for precursor_UUID in precursors:
            drug_name, logp = Precursors.objects.filter(UUID=precursor_UUID).values_list('DrugName', 'logp').first()
            precursor = PrecursorForMetaboliteView(drug_name, logp)
            self.precursors_to_metabolites[precursor] = []
            metabolite_UUIDs = get_metabolite_UUIDs(precursor_UUID, [])
            if metabolite_UUIDs is not None:
                metabolites = self.model.objects\
                    .filter(UUID__in=metabolite_UUIDs)\
                    .values_list('metabolite_InChiKey', 'biosystem', 'logp', 'enzyme', 'reaction')
                for item in metabolites:
                    inchi_key = item[0]
                    biosystem = item[1]
                    logp = item[2]
                    enzyme = item[3]
                    reaction = item[4]
                    metabolite = MetaboliteForMetaboliteView(inchi_key, biosystem, logp, enzyme, reaction)
                    self.precursors_to_metabolites[precursor].append(metabolite)
        response = []
        for precursor, metabolites in self.precursors_to_metabolites.items():
            if precursor.logp is None:
                precursor.logp = -1 * sys.float_info.max
            for metabolite in metabolites:
                if metabolite.logp is None:
                    metabolite.logp = -1 * sys.float_info.max
                response.append({
                    'drug_name': precursor.drug_name,
                    'precursor_logp': float(precursor.logp),
                    'metabolite_InChiKey': metabolite.inchi_key,
                    'biosystem': metabolite.biosystem,
                    'metabolite_logp': float(metabolite.logp),
                    'enzyme': metabolite.enzyme,
                    'reaction': metabolite.reaction,
                })
        context['precursors_to_metabolites'] = response
        return context

    def get_precursors(self):
        precursors = self.request.session.get('precursor_UUIDs')
        return precursors

    # def post(self, request):
    #     self.request.session['precursor_UUIDs'] = None
    #     post_response = self.request.POST.get('precursor_UUIDs')
    #     self.request.session['precursor_UUIDs'] = json.loads(post_response)
    #     return HttpResponse()


class PrecursorForMetaboliteView:
    def __init__(self, drug_name, logp):
        self.drug_name = drug_name
        self.logp = logp


class MetaboliteForMetaboliteView:
    def __init__(self, inchi_key, biosystem, logp, enzyme, reaction):
        self.inchi_key = inchi_key
        self.biosystem = biosystem
        self.logp = logp
        self.enzyme = enzyme
        self.reaction = reaction


def get_metabolite_UUIDs(precursor_UUID, previous_level_response):
    response = previous_level_response
    metabolites = PrecursorMetaboliteMap.objects.filter(precursor_UUID=precursor_UUID).all()
    if len(metabolites) == 0:
        return
    else:
        response.extend(o.metabolite_UUID for o in metabolites)
        for metabolite in metabolites:
            get_metabolite_UUIDs(metabolite.metabolite_UUID, response)
    return response
