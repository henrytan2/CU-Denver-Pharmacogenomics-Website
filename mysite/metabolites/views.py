from django.http import HttpResponse
from django.views import generic
from .models import Metabolite
from precursor_metabolite_map.models import PrecursorMetaboliteMap
from precursors.models import Precursors
from rest_framework.views import APIView
from rest_framework.response import Response
import sys
import json
from django.core.cache import cache


class MetaboliteView(generic.ListView):
    model = Metabolite
    template_name = 'metabolite.html'
    precursor_UUIDs = []
    precursors_to_metabolites = {}

    def get_context_data(self, **kwargs):
        context = super(MetaboliteView, self).get_context_data(**kwargs)
        while True:
            precursors_to_metabolites_filled = cache.get('precursors_to_metabolites_filled')
            if precursors_to_metabolites_filled:
                break
            continue
        metabolites = map_metabolites_to_precursors(self.precursors_to_metabolites)
        context['precursors_to_metabolites'] = metabolites
        return context

    def get_precursors(self):
        precursors = self.request.session.get('precursor_UUIDs')
        return precursors

    def map_precursors_to_metabolites(self, precursors, precursor_metabolite_map):
        precursor_metabolite_map.clear()
        cache.set('precursors_to_metabolites_filled', False)
        precursors_processed = 0
        for precursor_UUID in precursors:
            drug_name, logp = Precursors.objects.filter(UUID=precursor_UUID).values_list('DrugName', 'logp').first()
            precursor = PrecursorForMetaboliteView(precursor_UUID, drug_name, logp)
            precursor_metabolite_map[precursor] = []
            metabolite_UUIDs = get_metabolite_UUIDs(precursor_UUID, [])
            if metabolite_UUIDs is not None:
                metabolites = self.model.objects \
                    .filter(UUID__in=metabolite_UUIDs) \
                    .values_list('metabolite_InChiKey', 'biosystem', 'logp', 'enzyme', 'reaction')
                precursor_metabolite_map[precursor] = build_metabolite_for_template(metabolites)
            precursors_processed += 1
            percentage = int((precursors_processed / len(precursors)) * 100)
            cache.set('percentage_of_metabolites_filled', percentage)
        cache.set('precursors_to_metabolites_filled', True)

    def post(self, request):
        self.request.session['precursor_UUIDs'] = None
        post_response = self.request.POST.get('precursor_UUIDs')
        self.request.session['precursor_UUIDs'] = json.loads(post_response)
        precursors = self.get_precursors()
        self.map_precursors_to_metabolites(precursors, self.precursors_to_metabolites)
        return HttpResponse('metabolites:metabolite_index', {'precursor_UUIDs': self.request.session['precursor_UUIDs']})


class CheckMetabolites(APIView):
    def get(self, request):
        response = {
            'metabolites_filled': cache.get('precursors_to_metabolites_filled'),
            'percentage': cache.get('percentage_of_metabolites_filled'),
        }
        return Response(response)


class MetaboliteSingleView(generic.ListView):
    model = Metabolite
    template_name = 'metabolite.html'
    precursors_to_metabolites = {}

    def get_context_data(self, *, object_list=None, **kwargs):
        self.precursors_to_metabolites.clear()
        context = super(MetaboliteSingleView, self).get_context_data(**kwargs)
        single_precursor_UUID = self.request.session['single_precursor_UUID']
        drug_name, logp = Precursors.objects.filter(UUID=single_precursor_UUID).values_list('DrugName', 'logp').first()
        precursor = PrecursorForMetaboliteView(single_precursor_UUID, drug_name, logp)
        metabolites_UUIDs = get_metabolite_UUIDs(single_precursor_UUID, [])
        if metabolites_UUIDs is not None:
            metabolites = self.model.objects \
                .filter(UUID__in=metabolites_UUIDs) \
                .values_list('metabolite_InChiKey', 'biosystem', 'logp', 'enzyme', 'reaction')
            self.precursors_to_metabolites[precursor] = build_metabolite_for_template(metabolites)

        metabolites = map_metabolites_to_precursors(self.precursors_to_metabolites)
        context['precursors_to_metabolites'] = metabolites
        self.request.session['single_precursor_UUID'] = None
        return context

    def post(self, request):
        self.request.session['single_precursor_UUID'] = None
        self.request.session.modified = True
        single_precursor_UUID = self.request.POST.get('singlePrecursorUUID')
        self.request.session['single_precursor_UUID'] = single_precursor_UUID

        return HttpResponse('metabolites:metabolite_single', {'single_precursor_UUID': self.request.session['single_precursor_UUID']})


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


def build_metabolite_for_template(metabolites):
    response = []
    for item in metabolites:
        inchi_key = item[0]
        biosystem = item[1]
        logp = item[2]
        enzyme = item[3]
        reaction = item[4]
        metabolite = MetaboliteForMetaboliteView(inchi_key, biosystem, logp, enzyme, reaction)
        response.append(metabolite)
    return response


def map_metabolites_to_precursors(precursors_to_metabolites):
    response = []
    for precursor, metabolites in precursors_to_metabolites.items():
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
    return response


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
