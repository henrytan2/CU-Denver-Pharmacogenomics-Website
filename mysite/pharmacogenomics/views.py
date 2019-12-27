from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from .models import SideEffect
from .forms import DrugIDForm
from django_datatables_view.base_datatable_view import BaseDatatableView

# Create your views here.


class IndexView(generic.ListView):
    model = SideEffect
    template_name = 'pharmacogenomics/index.html'


class SideEffectView(generic.ListView):
    # form_class = DrugIDForm
    model = SideEffect
    template_name = 'pharmacogenomics/side-effect.html'

    def get_queryset(self):
        # side_effect_list = SideEffect.objects.values_list('side_effect', flat=True).distinct()
        return self.model.objects.values('side_effect').distinct()


