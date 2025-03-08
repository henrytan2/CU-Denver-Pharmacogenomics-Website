from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny

from .models import Metabolite
from precursors.models import Precursors
from full_metabolite_map.models import FullMetaboliteMap
from rest_framework.views import APIView
from rest_framework.response import Response
import sys


class GetMetabolitesViewForOnePrecursor(APIView):
    model = Metabolite
    precursors_to_metabolites = {}
    permission_classes = (AllowAny,)

    @swagger_auto_schema(auto_schema=None)
    def post(self, request):
        self.precursors_to_metabolites.clear()
        request_parsed = dict(self.request.data)
        precursor_uuids = request_parsed["precursorUUIDs"]
        drug_name, logp = Precursors.objects.filter(UUID__in=precursor_uuids).values_list('DrugName', 'logp').first()
        precursor = PrecursorForMetaboliteView(precursor_uuids, drug_name, logp)
        full_metabolite_maps = get_metabolite_Maps(precursor_uuids)
        metabolites_UUIDs = [o.metabolite_UUID for o in full_metabolite_maps]
        if metabolites_UUIDs is not None:
            metabolites = self.model.objects \
                .filter(UUID__in=metabolites_UUIDs)
            self.precursors_to_metabolites[precursor] = build_metabolite_for_template(metabolites)

        metabolites = map_metabolites_to_precursors(self.precursors_to_metabolites)
        return Response(metabolites)

class GetMetabolitesForMultiplePrecursors(APIView):
    model = Metabolite
    precursors_to_metabolites = {}
    permission_classes = (AllowAny,)

    def get_precursors(self):
        precursors = self.request.session.get('precursor_UUIDs')
        return precursors

    def map_precursors_to_metabolites(self, precursor_UUIDs, precursor_metabolite_map):
        precursor_metabolite_map.clear()
        full_metabolite_maps = get_metabolite_Maps(precursor_UUIDs)
        metabolite_UUIDs = [o.metabolite_UUID for o in full_metabolite_maps]
        metabolites = self.model.objects \
            .filter(UUID__in=metabolite_UUIDs)
        precursors = Precursors.objects.filter(UUID__in=precursor_UUIDs)
        for precursor_UUID in precursor_UUIDs:
            precursor = [p for p in precursors if p.UUID == precursor_UUID][0]
            drug_name = precursor.DrugName
            logp = precursor.logp
            precursor_for_view = PrecursorForMetaboliteView(precursor_UUID, drug_name, logp)
            precursor_metabolite_map[precursor_for_view] = []
            full_metabolite_maps_for_precursor = [o for o in full_metabolite_maps if o.precursor_UUID == precursor_UUID]
            metabolite_UUIDs_for_precursor = [o.metabolite_UUID for o in full_metabolite_maps_for_precursor]
            metabolites_for_precursor = [o for o in metabolites if o.UUID in metabolite_UUIDs_for_precursor]
            if metabolites_for_precursor is not None:
                precursor_metabolite_map[precursor_for_view] = build_metabolite_for_template(metabolites_for_precursor)

    @swagger_auto_schema(auto_schema=None)
    def post(self, request):
        request_parsed = dict(self.request.data)
        precursor_uuids = request_parsed["precursorUUIDs"]
        self.map_precursors_to_metabolites(precursor_uuids, self.precursors_to_metabolites)
        metabolites = map_metabolites_to_precursors(self.precursors_to_metabolites)
        return Response(metabolites)


def get_metabolite_Maps(precursor_UUIDs):
    response = []
    full_metabolite_maps = FullMetaboliteMap.objects.filter(precursor_UUID__in=precursor_UUIDs).all()
    if full_metabolite_maps is not None:
        response = full_metabolite_maps
    return response


def build_metabolite_for_template(metabolites):
    response = []
    for item in metabolites:
        inchi_key = item.metabolite_InChiKey
        biosystem = item.biosystem
        logp = item.logp
        enzyme = item.enzyme
        reaction = item.reaction
        metabolite_smile_string = item.metabolite_smile_string
        metabolite = MetaboliteForMetaboliteView(inchi_key, biosystem, logp, enzyme, reaction, metabolite_smile_string)
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
                'metabolite_smile_string': metabolite.metabolite_smile_string
            })
    return response


class PrecursorForMetaboliteView:
    def __init__(self, precursor_UUID, drug_name, logp):
        self.precursor_UUID = precursor_UUID
        self.drug_name = drug_name
        self.logp = logp


class MetaboliteForMetaboliteView:
    def __init__(self, inchi_key, biosystem, logp, enzyme, reaction, metabolite_smile_string):
        self.inchi_key = inchi_key
        self.biosystem = biosystem
        self.logp = logp
        self.enzyme = enzyme
        self.reaction = reaction
        self.metabolite_smile_string = metabolite_smile_string
