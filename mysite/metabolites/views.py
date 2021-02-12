from django.views import generic
from .models import Metabolite
from precursor_metabolite_map.models import PrecursorMetaboliteMap
from precursors.models import Precursors

# Create your views here.
class MultiplePrecursorView(generic.ListView):
    model = Metabolite
    template_name = 'multi-precursor.html'
    precursors_to_metabolites = {}

    def get_context_data(self, **kwargs):
        context = super(MultiplePrecursorView, self).get_context_data(**kwargs)
        precursors = self.get_list_of_precursors()
        for precursor_UUID in precursors:
            drug_name, inchi_key = Precursors.objects.filter(UUID=precursor_UUID).values_list('DrugName', 'InChiKey').first()
            precursor = PrecursorForMetaboliteView(drug_name, inchi_key)
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
            for metabolite in metabolites:
                if metabolite.logp == None:
                    metabolite.logp = 0
                response.append({
                    'drug_name': precursor.drug_name,
                    'precursor_InChiKey': precursor.inchi_key,
                    'metabolite_InChiKey': metabolite.inchi_key,
                    'biosystem': metabolite.biosystem,
                    'logp': float(metabolite.logp),
                    'enzyme': metabolite.enzyme,
                    'reaction': metabolite.reaction,
                })
        context['precursors_to_metabolites'] = response
        return context

    def get_list_of_precursors(self):
        # precursors = self.request.GET['precursors']
        precursors = ['47626af9-0953-49e1-bbd0-6ef9e5a03a6e']
        return precursors

class PrecursorForMetaboliteView:
    def __init__(self, drug_name, inchi_key):
        self.drug_name = drug_name
        self.inchi_key = inchi_key

class MetaboliteForMetaboliteView:
    def __init__(self, inchi_key, biosystem, logp, enzyme, reaction):
        self.inchi_key = inchi_key
        self.biosystem = biosystem
        self.logp = logp
        self.enzyme = enzyme
        self.reaction = reaction

# class SinglePrecursorView():
#     model = Metabolite
#     template_name = ''

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
