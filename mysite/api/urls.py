from django.urls import path, include
from .views import FasprPrepAPI
from .views import FasprRunAPI
from .views import MetabPrepAPI
from .views import CacheCCIDAPI
from .views import CachePositionsAPI
from .views import CacheLengthAPI
from .views import CacheProteinAPI
from .views import FindResolutionAPI
from .views import FindpLDDTAPI

app_name = 'api'

urlpatterns = [
    path(r'faspr-prep', FasprPrepAPI.as_view(), name='faspr_prep'),
    path(r'faspr-run', FasprRunAPI.as_view(), name='faspr_run'),
    path(r'metab-prep', MetabPrepAPI.as_view(), name='metab_prep'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path(r'pdbgen-results', include('pdbgen.urls')),
    path(r'cache-ccid', CacheCCIDAPI.as_view(), name='cache_CCID'),
    path(r'cache-positions', CachePositionsAPI.as_view(), name='cache_positions'),
    path(r'cache-length', CacheLengthAPI.as_view(), name='cache_length'),
    path(r'cache-protein-structure', CacheProteinAPI.as_view(), name='cache_protein_structure'),
    path(r'best-resolution', FindResolutionAPI.as_view(), name='best_resolution'),
    path(r'plddt-score', FindpLDDTAPI.as_view(), name='find_plddt'),
]
