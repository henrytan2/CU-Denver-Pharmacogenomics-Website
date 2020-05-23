from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.views import generic
from .models import SideEffect
import requests


class SideEffectView(generic.ListView):
    model = SideEffect
    template_name = 'side-effect.html'
    side_effect_list = []

    def get_queryset(self):
        return self.model.objects.values('side_effect').distinct()

    def post(self, request):
        if request.method == 'POST':
            self.side_effect_list = request.POST.getlist('sideEffectList[]')
            request.session['side_effect_list'] = self.side_effect_list
            return HttpResponse('pharmacogenomics:side-effect-results', {'side_effect_list': self.side_effect_list})


class SideEffectResultsView(generic.ListView):
    model = SideEffect
    template_name = 'side-effect-result.html'

    def get_queryset(self):
        session_side_effect_list = self.request.session.get('side_effect_list')
        return self.model.objects.filter(side_effect__in=session_side_effect_list)


class SideEffectRankedDrugsView(generic.ListView):
    model = SideEffect
    template_name = 'side-effect-drugs-ranked.html'

    def get_queryset(self):
        session_side_effect_list = self.request.session.get('side_effect_list')
        return self.model.objects.filter(side_effect__in=session_side_effect_list)\
            .values('drug_name', 'drug_id').annotate(dcount=Count('drug_name'))


class FDAInfoView(generic.TemplateView):
    template_name = 'fda.html'

    def post(self, request):
        drug_name = request.POST.get("drugName")

        if request.method == 'POST':
            fda_api_url = f'https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:"{drug_name}"&count=patient.reaction.reactionmeddrapt.exact '
            response = requests.get(fda_api_url).json()
            return JsonResponse(response, safe=False)