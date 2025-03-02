from django.urls import path
from . import views

app_name = 'metabolite'
urlpatterns = [
    path(r'get-metabolites-for-one-precursor', views.GetMetabolitesViewForOnePrecursor.as_view(), name='get_metabolites_for_one_precursor'),
    path(r'get-metabolites-for-multiple-precursors', views.GetMetabolitesForMultiplePrecursors.as_view(), name='get_metabolites_for_multiple_precursors'),
]
