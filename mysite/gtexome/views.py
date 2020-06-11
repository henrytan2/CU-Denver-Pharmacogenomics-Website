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
            if request.POST.get('filterRatio') is not None:
                filter_ratio_dict = request.POST.get('filterRatio')
                request.session['filter_ratio'] = json.loads(filter_ratio_dict)
                response = HttpResponse('gtexome:ratio_results', {'filter_ratio': filter_ratio_dict})
                return response
            else:
                filter_dict_str = request.POST.get('filterDictionary')
                self.filter_dictionary = json.loads(filter_dict_str)
                request.session['filter_dictionary'] = self.filter_dictionary
                return HttpResponse('gtexome:range_results', {'filter_dictionary': self.filter_dictionary})


class RangeResultsView(generic.ListView):
    model = GTEx
    template_name = 'range-results.html'

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


class RatioResultsView(generic.ListView):
    model = GTEx
    template_name = 'ratio-results.html'

    def get_queryset(self):
        session_filter_dictionary = self.request.session.get('filter_ratio')
        all_fields = self.model._meta.get_fields()
        all_fields_verbose = [f.verbose_name for f in all_fields]
        verbose_to_non_verbose_dict = {}
        for verbose, non_verbose in zip(all_fields_verbose, all_fields):
            verbose_to_non_verbose_dict[verbose] = non_verbose.attname

        verbose_tissues = session_filter_dictionary['tissues']
        numerator_tissues = [verbose_to_non_verbose_dict[tissue] for tissue in verbose_tissues]
        denominator_tissues = [tissue for tissue in verbose_to_non_verbose_dict.values()
                               if tissue not in numerator_tissues]
        denominator_tissues.remove('gene_id')
        denominator_tissues.remove('id')
        denominator_tissues.remove('description')
        lower_bound = float('-inf') if session_filter_dictionary['lower'] is None \
            else float(session_filter_dictionary['lower'])
        upper_bound = float('inf') if session_filter_dictionary['upper'] is None \
            else float(session_filter_dictionary['upper'])

        all_objs = self.model.objects.all()
        exclude_objs = []
        ratios = {}
        for obj in all_objs:
            numerator = 0
            denominator = 0
            for num_tissue in numerator_tissues:
                numerator += getattr(obj, num_tissue)

            for den_tissue in denominator_tissues:
                denominator += getattr(obj, den_tissue)
            if numerator == 0:
                exclude_objs.append(obj)
                continue
            if denominator == 0:
                exclude_objs.append(obj)
                continue
            ratio = numerator / denominator
            ratios[obj.gene_id] = ratio
            if not (lower_bound <= ratio <= upper_bound):
                exclude_objs.append(obj.gene_id)

        all_objs = all_objs.exclude(gene_id__in=exclude_objs)
        for obj in all_objs:
            obj.ratio = ratios[obj.gene_id]
        return all_objs


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
