from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path(r'faspr-prep', views.FasprPrepAPI.as_view(), name='faspr_prep'),
]