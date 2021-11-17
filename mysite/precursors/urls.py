from django.urls import path
from . import views

app_name = 'precursors'
urlpatterns = [
    path(r'fetchall', views.FetchAllPrecursorsAPI.as_view(), name='fetch_all_precursors'),
    path(r'precursor_results', views.PrecursorsTemplateView.as_view(), name='precursor_results'),
    path(r'fetch_for_precursor_results', views.PrecursorFetchAPIView.as_view(), name='fetch_for_precursor_results'),
    path(r'receive_precursors_selected', views.ReceivePrecursorsSelectedAPI.as_view(), name='receive_precursors_selected'),
]
