from django.urls import path, include

from .views import FasprPrepAPI, FasprPrepPublicAPI
from .views import FasprRunAPI
from .views import MetabPrepAPI
from .views import FindResolutionAPI
from .views import FindPlddtAPI, FindPlddtPublicAPI, FindResolutionPublicAPI, FasprPrepUploadFileAPI
from .business.plotly_trial import mutation_app # need to keep

app_name = 'api'

urlpatterns = [
    path('faspr-prep', FasprPrepAPI.as_view(), name='faspr_prep'),
    path('faspr-run', FasprRunAPI.as_view(), name='faspr_run'),
    path('metab-prep', MetabPrepAPI.as_view(), name='metab_prep'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('pdbgen-results', include('pdbgen.urls')),
    path('best-resolution', FindResolutionAPI.as_view(), name='/best_resolution'),
    path('plddt-score', FindPlddtAPI.as_view(), name='find_plddt'),
    path('public-plddt-score', FindPlddtPublicAPI.as_view(), name='public_find_plddt'),
    path('public-best-resolution', FindResolutionPublicAPI.as_view(), name='public_best_resolution'),
    path('public-faspr-prep', FasprPrepPublicAPI.as_view(), name='public_faspr_prep'),
    path('faspr-prep-file-upload', FasprPrepUploadFileAPI.as_view(), name='faspr-prep-upload-file'),
]
