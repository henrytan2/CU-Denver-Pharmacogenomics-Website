from django.urls import path
from . import views

app_name = 'pharmacogenomics'
urlpatterns = [
    path('side-effect/', views.SideEffectView.as_view(), name='side-effect'),
    path('results/', views.SideEffectResultsView.as_view(), name='side-effect-results'),
    path('drugs-ranked/', views.SideEffectRankedDrugsView.as_view(), name='side-effect-ranked-drugs'),
    path('ranked-drugs', views.DrugsRankedAPI.as_view(), name='ranked-drugs'),
    path(r'fda/', views.FDAInfoView.as_view(), name='fda'),
    path(r'get-side-effects/', views.GetSideEffects.as_view(), name='get-side-effects'),
    path(r'get-drugs-by-selected-sideeffects', views.GetDrugsFromSelectedSideEffects.as_view(), name='get-drugs-by-selected-sideeffects')
]
