from django.urls import path
from . import views

app_name = 'pdbgen'
urlpatterns = [
    path(r'', views.IndexView.as_view(), name='pdbgen_index'),
]
