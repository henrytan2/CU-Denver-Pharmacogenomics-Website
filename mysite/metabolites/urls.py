from django.urls import path

from . import views

app_name = 'metabolite'
urlpatterns = [
    path(r'multi-precursor/', views.MultiplePrecursorView.as_view(), name='metabolites'),
    # path(r'single-precursor/', views.SinglePrecursorView.as_view(), name='metabolites'),
]
