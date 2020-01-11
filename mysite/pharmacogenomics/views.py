from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from .models import SideEffect


class IndexView(generic.TemplateView):
    template_name = 'pharmacogenomics/index.html'


class SideEffectView(generic.ListView):
    model = SideEffect
    template_name = 'pharmacogenomics/side-effect.html'
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
    template_name = 'pharmacogenomics/side-effect-result.html'

    def get_queryset(self):
        session_side_effect_list = self.request.session.get('side_effect_list')
        return self.model.objects.filter(side_effect__in=session_side_effect_list)


class SideEffectRankedDrugsView(generic.ListView):
    model = SideEffect
    template_name = 'pharmacogenomics/side-effect-drugs-ranked.html'

    def get_queryset(self):
        session_side_effect_list = self.request.session.get('side_effect_list')
        return self.model.objects.filter(side_effect__in=session_side_effect_list)\
            .values('drug_name').annotate(dcount=Count('drug_name'))


class ContactView(generic.ListView):
    model = SideEffect
    template_name = 'pharmacogenomics/contact.html'
