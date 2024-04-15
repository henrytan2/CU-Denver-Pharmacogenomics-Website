from django.urls import path
from . import views

app_name = 'metabolite'
urlpatterns = [
    path(r'get-metabolites-for-one-precursor', views.GetMetabolitesViewForOnePrecursor.as_view(), name='get_metabolites_for_one_precursor'),
    path(r'', views.MetaboliteView.as_view(), name='metabolite_index'),
    path(r'single/', views.MetaboliteSingleView.as_view(), name='metabolite_single'),
    path(r'check/', views.CheckMetabolites.as_view(), name='check')
]
