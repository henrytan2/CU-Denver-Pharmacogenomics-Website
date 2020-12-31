from django.urls import path

from . import views

app_name = 'metabolite'
urlpatterns = [
    path(r'', views.IndexView.as_view(), name='metabolites'),
]
