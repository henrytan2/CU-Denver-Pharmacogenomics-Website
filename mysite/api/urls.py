from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
    path(r'faspr-prep', views.FasprPrepAPI.as_view(), name='faspr_prep'),
    path(r'metab-prep', views.MetabPrepAPI.as_view(), name='metab_prep'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),

]