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
        return self.model.objects.filter(side_effect='Abdominal pain')

def get_gene_id(request):
    if request.method == 'POST':
        form = DrugIDForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("url 'pharmacogenomics:side-effect'")
        else:
            form = DrugIDForm()
        return render(request, 'pharmacogenomics/index.html', {'form': form})

