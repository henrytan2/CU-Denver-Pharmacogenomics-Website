from django.http import HttpResponse, JsonResponse
from django.views import generic

from .models import GTEx
import requests
import json

class IndexView(generic.ListView):
    model = GTEx
    template_name = 'gtexome.html'
    filter_dictionary = []

    def get_queryset(self):
        all_fields = self.model._meta.get_fields()
        do_not_include = ['ID', 'Gene ID', 'Description']
        all_field_names = [f.verbose_name for f in all_fields]
        for item in do_not_include:
            all_field_names.remove(item)
        return all_field_names

    def post(self, request):
        if request.method == 'POST':
            filter_dict_str = request.POST.get('filterDictionary')
            self.filter_dictionary = json.loads(filter_dict_str)
            request.session['filter_dictionary'] = self.filter_dictionary
            return HttpResponse('gtexome:results', {'filter_dictionary': self.filter_dictionary})


class ResultsView(generic.ListView):
    model = GTEx
    template_name = 'results.html'

    def get_queryset(self):
        session_filter_dictionary = self.request.session.get('filter_dictionary')
        all_fields = self.model._meta.get_fields()
        all_fields_verbose = [f.verbose_name for f in all_fields]
        verbose_to_non_verbose_dict = {}
        for verbose, non_verbose in zip(all_fields_verbose, all_fields):
            verbose_to_non_verbose_dict[verbose] = non_verbose
        filter_non_verbose = {}

        for session_filter in session_filter_dictionary:
            tissue = session_filter['tissue']
            if tissue in verbose_to_non_verbose_dict.keys():
                tissue_str = str(verbose_to_non_verbose_dict[tissue])[13:]
                filter_non_verbose[tissue_str] = session_filter['range']
        kwargs = {}
        for tissue, filter_range in filter_non_verbose.items():
            kwargs['{0}__{1}'.format(str(tissue), 'gte')] = float(filter_range['lower'])
            kwargs['{0}__{1}'.format(str(tissue), 'lte')] = float(filter_range['upper'])
        return self.model.objects.filter(**kwargs)


class ExomeView(generic.TemplateView):
    template_name = 'exome.html'
    exac_data = ''

    def post(self, request):
        exac_api_url = 'http://exac.hms.harvard.edu/rest/gene/variants_in_transcript/'
        gene_id = request.POST.get("geneID")
        if request.method == 'POST':
            url = "{0}{1}".format(exac_api_url, gene_id)
            self.exac_data = requests.get(url).json()
            return JsonResponse(self.exac_data, safe=False)
