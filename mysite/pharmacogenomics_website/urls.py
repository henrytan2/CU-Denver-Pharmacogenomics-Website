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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
import os

environment = os.getenv('DJANGO_ENV')

if settings.DEBUG:
    API_ROUTE = ''
    BASE_URL = 'http://localhost:8000'
else:
    API_ROUTE = 'api/'
    BASE_URL = 'https://pharmacogenomics.clas.ucdenver.edu' if environment == 'production' else 'http://localhost'

print(f'IN DEBUG MODE: {settings.DEBUG}')
print(f'DJANGO ENV: {environment}')

schema_view = get_schema_view(
    openapi.Info(
        title="CU Denver Pharmacogenomics API",
        default_version='v1',
        description="API documentation for CU Denver Pharmacogenomics Website",
    ),
    public=True,
    url='https://pharmacogenomics.clas.ucdenver.edu',
    permission_classes=[permissions.AllowAny,],
)


urlpatterns = [
    path(f'{API_ROUTE}admin/', admin.site.urls),
    path(f'{API_ROUTE}api/', include('api.urls')),
    path(f'{API_ROUTE}pharmacogenomics/', include('pharmacogenomics.urls')),
    path(f'{API_ROUTE}gtexome/', include('gtexome.urls')),
    path(f'{API_ROUTE}metabolites/', include('metabolites.urls')),
    path(f'{API_ROUTE}precursors/', include('precursors.urls')),
    path(f'{API_ROUTE}pdbgen-backend/', include('pdbgen.urls')),
    path(f'{API_ROUTE}django_plotly_dash/', include('django_plotly_dash.urls')),
    path(f'{API_ROUTE}accounts/', include('django.contrib.auth.urls')),
    path(f'{API_ROUTE}user_accounts/', include('user_accounts.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
    ]