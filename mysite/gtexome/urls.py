from django.urls import path

from . import views

app_name = 'gtexome'
urlpatterns = [
    path('', views.IndexView.as_view(), name='gtexome'),
    path('range-results/', views.RangeResultsView.as_view(), name='range_results'),
    path('ratio-results/', views.RatioResultsView.as_view(), name='ratio_results'),
    path(r'exome/', views.ExomeView.as_view(), name='exome'),
]
