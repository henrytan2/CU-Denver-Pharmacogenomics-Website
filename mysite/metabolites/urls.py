from django.urls import path

from . import views

app_name = 'metabolite'
urlpatterns = [
    path(r'', views.MetaboliteView.as_view(), name='metabolite_index'),
]
