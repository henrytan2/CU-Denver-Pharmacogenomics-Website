from django.http import HttpResponse
from django.views import generic
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import GTEx
import requests
import json
from .business.exome import ExomeColumns

class GetTissueTypes(APIView):
    model = GTEx
    permission_classes = (AllowAny,)

    @swagger_auto_schema(auto_schema=None)
    def get(self, request):
        all_fields = self.model._meta.get_fields()
        do_not_include = ['ID', 'Gene ID', 'Description']
        all_field_names = [f.verbose_name for f in all_fields]
        for item in do_not_include:
            all_field_names.remove(item)
        return Response(all_field_names)

class GetRangeResults(APIView):
    model = GTEx
    permission_classes = (AllowAny,)

    @swagger_auto_schema(auto_schema=None)
    def post(self, request):
        filter_list = list(self.request.data)
        all_fields = self.model._meta.get_fields()
        all_fields_verbose = {f.verbose_name for f in all_fields}
        verbose_to_non_verbose_dict = {}
        for verbose, non_verbose in zip(all_fields_verbose, all_fields):
            verbose_to_non_verbose_dict[verbose] = non_verbose

        filter_non_verbose = {}
        for filter in filter_list:
            tissue = filter['tissue']
            if tissue in verbose_to_non_verbose_dict.keys():
                tissue_str = str(verbose_to_non_verbose_dict[tissue])[13:]
                filter_non_verbose[tissue_str] = filter['range']
        kwargs = {}
        for tissue, filter_range in filter_non_verbose.items():
            if (filter_range['upper']) == '' or (filter_range['upper']) is None:
                filter_range['upper'] = 10000000
            if (filter_range['lower']) == '' or (filter_range['lower']) is None:
                filter_range['lower'] = 0
            kwargs['{0}__{1}'.format(str(tissue), 'gte')] = float(filter_range['lower'])
            kwargs['{0}__{1}'.format(str(tissue), 'lte')] = float(filter_range['upper'])
        response = []
        for obj in self.model.objects.filter(**kwargs):
            response.append({
                'gene_id': obj.gene_id,
                'description': obj.description
            })
        return Response(response)

class GetRatioResults(APIView):
    model = GTEx
    permission_classes = (AllowAny,)

    @swagger_auto_schema(auto_schema=None)
    def post(self, request):
        all_fields = self.model._meta.get_fields()
        all_fields_verbose = [f.verbose_name for f in all_fields]
        verbose_to_non_verbose_dict = {}
        for verbose, non_verbose in zip(all_fields_verbose, all_fields):
            verbose_to_non_verbose_dict[verbose] = non_verbose.attname
        ratio_request = dict(self.request.data)
        verbose_tissues = ratio_request['tissues']
        numerator_tissues = [verbose_to_non_verbose_dict[tissue] for tissue in verbose_tissues]
        denominator_tissues = [tissue for tissue in verbose_to_non_verbose_dict.values()
                               if tissue not in numerator_tissues]
        denominator_tissues.remove('gene_id')
        denominator_tissues.remove('id')
        denominator_tissues.remove('description')
        lower_bound = float('-inf') if ratio_request['lower'] is None \
            else float(ratio_request['lower'])
        upper_bound = float('inf') if ratio_request['upper'] is None \
            else float(ratio_request['upper'])

        all_objs = set(self.model.objects.all())
        exclude_objs = set()
        ratios = {}
        for obj in all_objs:
            numerator = 0
            denominator = 0
            for num_tissue in numerator_tissues:
                numerator += getattr(obj, num_tissue)

            for den_tissue in denominator_tissues:
                denominator += getattr(obj, den_tissue)
            if numerator == 0:
                exclude_objs.add(obj)
                continue
            if denominator == 0:
                exclude_objs.add(obj)
                continue
            ratio = numerator / denominator
            ratios[obj.gene_id] = ratio
            if not (lower_bound <= ratio <= upper_bound):
                exclude_objs.add(obj)

        excluded_objs = all_objs - exclude_objs
        response = []
        for obj in excluded_objs:
            ratio = ratios[obj.gene_id]
            gene_id = obj.gene_id
            description = obj.description
            response.append({
                'ratio': ratio,
                'gene_id': gene_id,
                'description': description,
            })
        return Response(response)

class IndexView(generic.ListView):
    model = GTEx
    template_name = 'gtexome.html'
    filter_dictionary = []

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # move to api view start
        all_fields = self.model._meta.get_fields()
        do_not_include = ['ID', 'Gene ID', 'Description']
        all_field_names = [f.verbose_name for f in all_fields]
        for item in do_not_include:
            all_field_names.remove(item)
            #move to api view end
            # return Response(all_field_names)
        context['all_field_names'] = all_field_names
        return context

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
            if (filter_range['upper']) == '' or (filter_range['upper']) is None:
                filter_range['upper'] = 10000000
            if (filter_range['lower']) == '' or (filter_range['lower']) is None:
                filter_range['lower'] = 0
            kwargs['{0}__{1}'.format(str(tissue), 'gte')] = float(filter_range['lower'])
            kwargs['{0}__{1}'.format(str(tissue), 'lte')] = float(filter_range['upper'])
        response = []
        for obj in self.model.objects.filter(**kwargs):
            response.append({
                'gene_id': obj.gene_id,
                'description': obj.description
            })
        return response


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

        all_objs = set(self.model.objects.all())
        exclude_objs = set()
        ratios = {}
        for obj in all_objs:
            numerator = 0
            denominator = 0
            for num_tissue in numerator_tissues:
                numerator += getattr(obj, num_tissue)

            for den_tissue in denominator_tissues:
                denominator += getattr(obj, den_tissue)
            if numerator == 0:
                exclude_objs.add(obj)
                continue
            if denominator == 0:
                exclude_objs.add(obj)
                continue
            ratio = numerator / denominator
            ratios[obj.gene_id] = ratio
            if not (lower_bound <= ratio <= upper_bound):
                exclude_objs.add(obj)

        excluded_objs = all_objs - exclude_objs
        response = []
        for obj in excluded_objs:
            ratio = ratios[obj.gene_id]
            gene_id = obj.gene_id
            description = obj.description
            response.append({
                'ratio': ratio,
                'gene_id': gene_id,
                'description': description,
            })
        return response


class ExomeView(generic.TemplateView):
    template_name = 'exome.html'
    gnomad_data = ''

    def get_context_data(self, **kwargs):
        context = super(ExomeView, self).get_context_data(**kwargs)
        context['gnomad_data'] = self.make_request_to_gnomad()
        context['exome_columns'] = ExomeColumns.Get
        return context

    def make_request_to_gnomad(self):
        gene_id = self.request.GET['gene_id']
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
              lof_curation{
                verdict
                }
              }      
            }
          }
        """
        query = query % gene_id

        url = 'https://gnomad.broadinstitute.org/api/'
        response = json.dumps(requests.post(url, json={'query': query}).json())
        return response


class ExacView(generic.TemplateView):
    template_name = 'exac-results.html'
    gnomad_data = ''

    def get_context_data(self, **kwargs):
        context = super(ExacView, self).get_context_data(**kwargs)
        context['gnomad_data'] = self.make_request_to_gnomad()
        context['exome_columns'] = ExomeColumns.Get
        return context

    def make_request_to_gnomad(self):
        gene_id = self.request.GET['gene_symbol']
        query = """query {
          gene(gene_symbol: "%s", reference_genome: GRCh37) {
            variants(dataset: gnomad_r2_1) {
              gene_id
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

        url = 'https://gnomad.broadinstitute.org/api/'
        response = json.dumps(requests.post(url, json={'query': query}).json())
        return response
