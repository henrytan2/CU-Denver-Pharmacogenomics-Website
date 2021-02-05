from django.views import generic
from .models import Metabolite
from mysite.precursor_metabolite_map.models import PrecursorMetaboliteMap


# Create your views here.
class MultiplePrecursorView(generic.ListView):
    model = Metabolite
    template_name = 'metabolites.html'
    precursors_to_metabolites = {}

    def get_context_data(self, **kwargs):
        context = super(MultiplePrecursorView, self).get_context_data(**kwargs)
        precursors = self.get_list_of_precursors()
        for precursor_UUID in precursors:
            self.precursors_to_metabolites[precursor_UUID] = []
            metabolite_UUIDs = get_metabolite_UUIDs(precursor_UUID, [])
            if metabolite_UUIDs is not None:
                metabolites = self.model.objects.filter(UUID__in=metabolite_UUIDs)
                self.precursors_to_metabolites[precursor_UUID].extend(metabolites)

    def get_list_of_precursors(self):
        # precursors = self.request.GET['precursors']
        precursors = ['01b41b94-0d84-47b0-83b4-cfc0f247a236', '01b41b94-0d84-47b0-83b4-cfc0f247a236']
        return precursors



# class SinglePrecursorView():
#     model = Metabolite
#     template_name = ''

def get_metabolite_UUIDs(precursor_UUID, previous_level_response):
    response = previous_level_response
    metabolites = PrecursorMetaboliteMap.objects.get(precursor_UUID=precursor_UUID)
    if (len(metabolites) == 0):
        return
    else:
        response.extend(metabolites)
        for metabolite in metabolites:
            get_metabolite_UUIDs(metabolite.metabolite_UUID, response)
    return response