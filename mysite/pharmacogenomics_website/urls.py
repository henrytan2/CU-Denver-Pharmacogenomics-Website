"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.authtoken import views as rest_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', views.IndexView.as_view(), name='index'),
    path('people/', views.PeopleView.as_view(), name='people'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('pharmacogenomics/', views.IndexView.as_view(), name='index2'),
    path('pharmacogenomics/', include('pharmacogenomics.urls')),
    path('gtexome/', include('gtexome.urls')),
    path('metabolites/', include('metabolites.urls')),
    path('precursors/', include('precursors.urls')),
    path('pdbgen-backend/', include('pdbgen.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('api-token-auth/', rest_views.obtain_auth_token),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user_accounts/', include('user_accounts.urls')),
    path('esnuel', include('esnuel.urls'))
    ]