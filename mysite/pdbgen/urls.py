from django.urls import path
from . import views

app_name = 'pdbgen-backend'
urlpatterns = [
    path('pdbgen-results/', views.read_CCID, name='pdbgen-results.html'),
    path(r'save-data', views.store_pdbgen_data, name='pdbgen_save')
]
