from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.views import generic
from .models import SideEffect
from precursors.models import Precursors
from drug_name_precursor_map.models import DrugNamePrecursorMap
import requests
import json


class SideEffectView(generic.ListView):
    model = SideEffect
    template_name = 'side-effect.html'
    side_effect_list = []

    def get_queryset(self):
        side_effects = self.model.objects.values('side_effect').distinct()
        response = list(side_effects)
        return response

    def post(self, request):
        if request.method == 'POST':
            self.side_effect_list = request.POST.getlist('sideEffectList[]')
            request.session['side_effect_list'] = self.side_effect_list
            return HttpResponse('pharmacogenomics:side-effect-results', {'side_effect_list': self.side_effect_list})


class SideEffectResultsView(generic.ListView):
    model = SideEffect
    template_name = 'side-effect-result.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SideEffectResultsView, self).get_context_data(**kwargs)
        session_side_effect_list = self.request.session.get('side_effect_list')
        drugs = self.model.objects.filter(side_effect__in=session_side_effect_list).values()
        drug_ids = []
        for drug in drugs:
            drug_ids.append(drug['drug_id'])
        precursors = DrugNamePrecursorMap.objects.filter(precursor_DrugID__in=drug_ids)
        precursor_dict = {}
        for precursor in precursors:
            precursor_dict[precursor.precursor_DrugID] = precursor
        for drug in drugs:
            drug['UUID'] = precursor_dict[drug['drug_id']].precursor_UUID
        context['side_effect_results'] = list(drugs)
        return context


class SideEffectRankedDrugsView(generic.ListView):
    model = SideEffect
    template_name = 'side-effect-drugs-ranked.html'

    def get_context_data(self,  **kwargs):
        context = super(SideEffectRankedDrugsView, self).get_context_data(**kwargs)
        session_side_effect_list = self.request.session.get('side_effect_list')
        drugs = self.model.objects.filter(side_effect__in=session_side_effect_list)\
            .values('drug_name', 'drug_id').annotate(dcount=Count('drug_name'))
        drug_ids = []
        for drug in drugs:
            drug_ids.append(drug['drug_id'])
        precursors = DrugNamePrecursorMap.objects.filter(precursor_DrugID__in=drug_ids)
        precursor_dict = {}
        for precursor in precursors:
            precursor_dict[precursor.precursor_DrugID] = precursor
        response = []
        for drug in drugs:
            response.append({
                'UUID': precursor_dict[drug['drug_id']].precursor_UUID,
                'drug_name': drug['drug_name'],
                'drug_id': drug['drug_id'],
                'dcount': drug['dcount'],
            })
        context['drugs_ranked'] = response
        return context


class FDAInfoView(generic.TemplateView):
    template_name = 'fda.html'

    def get_context_data(self, **kwargs):
        context = super(FDAInfoView, self).get_context_data(**kwargs)
        drug_name = self.request.GET['drug_name']
        fda_api_url = f'https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:"{drug_name}"&count=patient.reaction.reactionmeddrapt.exact'
        response = requests.get(fda_api_url).json()
        context['fda_data'] = response
        return context
