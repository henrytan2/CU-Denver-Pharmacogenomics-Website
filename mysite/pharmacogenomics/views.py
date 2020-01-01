from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.views import generic
from .models import SideEffect
from django.db.models import Q

class IndexView(generic.ListView):
    model = SideEffect
    template_name = 'pharmacogenomics/index.html'


class SideEffectView(generic.ListView):
    model = SideEffect
    template_name = 'pharmacogenomics/side-effect.html'

    def get_queryset(self):
        return self.model.objects.values('side_effect').distinct()


class SideEffectResultsView(generic.ListView):
    model = SideEffect
    template_name = 'pharmacogenomics/side-effect-result.html'
    side_effect_list = []

    def post(self, request):
        if request.method == 'POST':
            self.side_effect_list = request.POST.getlist('sideEffectList[]')
            self.object_list = self.model.objects.filter(side_effect__in=self.side_effect_list)
            return HttpResponse('pharmacogenomics:side-effect-results', {'side_effect_list': self.side_effect_list})


class ContactView(generic.ListView):
    model = SideEffect
    template_name = 'pharmacogenomics/contact.html'
