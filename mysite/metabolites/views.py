from django.http import HttpResponse
from django.views import generic
from .models import Metabolite
from precursor_metabolite_map.models import PrecursorMetaboliteMap
from precursors.models import Precursors
import sys
import json
from django.core.cache import cache

# Create your views here.
class MetaboliteView(generic.ListView):
    model = Metabolite
    template_name = 'metabolite.html'
    precursor_UUIDs = []
    precursors_to_metabolites = {}

    def get_context_data(self, **kwargs):
        context = super(MetaboliteView, self).get_context_data(**kwargs)
        response = []
        single_precursor_UUID = self.request.session['single_precursor_UUID']
        if single_precursor_UUID is None:
            while True:
                precursors_to_metabolites_filled = cache.get('precursors_to_metabolites_filled')
                if precursors_to_metabolites_filled:
                    break
                continue
        if single_precursor_UUID is None:
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
        else:
            single_precursor_to_metabolites = {}
            self.map_precursors_to_metabolites([single_precursor_UUID], single_precursor_to_metabolites)
            for precursor in single_precursor_to_metabolites.keys():
                if precursor.precursor_UUID == single_precursor_UUID:
                    single_precursor = precursor
            metabolites = single_precursor_to_metabolites[single_precursor]
            if single_precursor.logp is None:
                single_precursor.logp = -1 * sys.float_info.max
            for metabolite in metabolites:
                if metabolite.logp is None:
                    metabolite.logp = -1 * sys.float_info.max
                response.append({
                    'drug_name': single_precursor.drug_name,
                    'precursor_logp': float(single_precursor.logp),
                    'metabolite_InChiKey': metabolite.inchi_key,
                    'biosystem': metabolite.biosystem,
                    'metabolite_logp': float(metabolite.logp),
                    'enzyme': metabolite.enzyme,
                    'reaction': metabolite.reaction,
                })
            context['precursors_to_metabolites'] = response
            self.request.session['single_precursor_UUID'] = None
        return context

    def map_precursors_to_metabolites(self, precursors, precursor_metabolite_map):
        precursor_metabolite_map.clear()
        cache.set('precursors_to_metabolites_filled', False)
        for precursor_UUID in precursors:
            drug_name, logp = Precursors.objects.filter(UUID=precursor_UUID).values_list('DrugName', 'logp').first()
            precursor = PrecursorForMetaboliteView(precursor_UUID, drug_name, logp)
            precursor_metabolite_map[precursor] = []
            metabolite_UUIDs = get_metabolite_UUIDs(precursor_UUID, [])
            if metabolite_UUIDs is not None:
                metabolites = self.model.objects \
                    .filter(UUID__in=metabolite_UUIDs) \
                    .values_list('metabolite_InChiKey', 'biosystem', 'logp', 'enzyme', 'reaction')
                for item in metabolites:
                    inchi_key = item[0]
                    biosystem = item[1]
                    logp = item[2]
                    enzyme = item[3]
                    reaction = item[4]
                    metabolite = MetaboliteForMetaboliteView(inchi_key, biosystem, logp, enzyme, reaction)
                    precursor_metabolite_map[precursor].append(metabolite)
        cache.set('precursors_to_metabolites_filled', True)

    def get_precursors(self):
        precursors = self.request.session.get('precursor_UUIDs')
        return precursors

    def post(self, request):
        self.request.session['precursor_UUIDs'] = None
        fill = json.loads(self.request.POST.get('fill'))
        if fill:
            self.request.session['single_precursor_UUID'] = None
            self.request.session.modified = True
            post_response = self.request.POST.get('precursor_UUIDs')
            self.request.session['precursor_UUIDs'] = json.loads(post_response)
            precursors = self.get_precursors()
            self.map_precursors_to_metabolites(precursors, self.precursors_to_metabolites)
        else:
            self.request.session['single_precursor_UUID'] = None
            self.request.session.modified = True
            single_precursor_UUID = self.request.POST.get('singlePrecursorUUID')
            self.request.session['single_precursor_UUID'] = single_precursor_UUID

        return HttpResponse('metabolites:metabolite_index', {'precursor_UUIDs': self.request.session['precursor_UUIDs']})


class PrecursorForMetaboliteView:
    def __init__(self, precursor_UUID, drug_name, logp):
        self.precursor_UUID = precursor_UUID
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
