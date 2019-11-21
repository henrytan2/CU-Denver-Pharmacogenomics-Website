from django.urls import path
from . import views

app_name = 'pharmacogenomics'
urlpatterns = [
    path('side-effect/', views.SideEffectView.as_view(), name='side-effect'),
    path('', views.IndexView.as_view(), name='index'),
]
