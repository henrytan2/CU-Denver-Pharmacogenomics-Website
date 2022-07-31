from django.shortcuts import render
from django.views import generic
from django.template.response import TemplateResponse


class IndexView(generic.TemplateView):
    template_name = 'pdbgen_index.html'


class ResultsView(generic.TemplateView):
    template_name = 'pdbgen_results.html'

def read_CCID():
    template_name = 'pdbgen_results.html'
    context = {'data':'\'{"mutation":{"value": "CCID_out"}}\''}
    return context
    # return render(request,'pdbgen_results.html',context)