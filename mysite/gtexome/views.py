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
    gnomad_data = ''

    def post(self, request):
        gene_id = request.POST.get("geneID")

        query = """query {
  gene(gene_id: "%s", reference_genome: GRCh37) {
    variants(dataset: gnomad_r2_1) {
      variantId
      exome {
        ac
        ac_hemi
        ac_hom
        an
        af
        filters
        populations {
          id
          ac
          an
        }
      }
      flags
      chrom
      pos
      alt
      consequence
      consequence_in_canonical_transcript
      hgvs
      hgvsc
      hgvsp
      lof
      lof_filter
      lof_flags
      rsid
      }      
    }
  }
"""

        query = query % gene_id

        if request.method == 'POST':
            url = 'https://gnomad.broadinstitute.org/api/'
            self.gnomad_data = requests.post(url, json={'query': query}).json()
            return JsonResponse(self.gnomad_data, safe=False)
