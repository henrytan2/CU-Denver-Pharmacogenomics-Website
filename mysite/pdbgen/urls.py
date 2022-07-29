from django.urls import path
from . import views

app_name = 'pdbgen'
urlpatterns = [
    path(r'', views.IndexView.as_view(), name='pdbgen_index'),
    path(r'pdbgen-results', views.ResultsView.as_view(), name='pdbgen-results.html'),
    # path('pdbgen-results_CCID', views.read_CCID, name='pdbgen-results.html'),
    # path('', views.read_CCID, name='reading-CCID'),
]
