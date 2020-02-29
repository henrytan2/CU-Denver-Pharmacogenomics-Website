from django.urls import path
from . import views

app_name = 'pharmacogenomics'
urlpatterns = [
    path('side-effect/', views.SideEffectView.as_view(), name='side-effect'),
    path('sider-searcher/results/', views.SideEffectResultsView.as_view(), name='side-effect-results'),
    path('sider-searcher/drugs-ranked/', views.SideEffectRankedDrugsView.as_view(), name='side-effect-ranked-drugs'),
]
