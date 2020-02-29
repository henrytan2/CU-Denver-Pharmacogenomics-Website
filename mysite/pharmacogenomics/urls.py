from django.urls import path
from . import views

app_name = 'pharmacogenomics'
urlpatterns = [
    path('side-searcher/', views.SideEffectView.as_view(), name='side-effect'),
    path('side-searcher/results/', views.SideEffectResultsView.as_view(), name='side-effect-results'),
    path('side-searcher/drugs-ranked/', views.SideEffectRankedDrugsView.as_view(), name='side-effect-ranked-drugs'),
]
