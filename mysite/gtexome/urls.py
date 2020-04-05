from django.urls import path

from . import views

app_name = 'gtexome'
urlpatterns = [
    path('', views.IndexView.as_view(), name='gtexome'),
    path('results/', views.ResultsView.as_view(), name='results'),
    path(r'exome/', views.ExomeView.as_view(), name='exome'),
]
