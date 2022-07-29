from django.urls import path, include
from .views import FasprPrepAPI
from .views import MetabPrepAPI
from .views import CacheCCIDAPI

app_name = 'api'

urlpatterns = [
    path(r'faspr-prep', FasprPrepAPI.as_view(), name='faspr_prep'),
    path(r'metab-prep', MetabPrepAPI.as_view(), name='metab_prep'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path(r'pdbgen-results', include('pdbgen.urls')),
    path(r'cache-ccid', CacheCCIDAPI.as_view(), name='cache_CCID'),
]