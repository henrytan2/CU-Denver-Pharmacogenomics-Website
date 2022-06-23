from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path(r'faspr-prep', views.FasprPrepAPI.as_view(), name='faspr_prep'),
    path(r'metab-prep', views.MetabPrepAPI.as_view(), name='metab_prep'),
]