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
import sys

sys.path.append("..")
from ..pharmacogenomics.views import SideEffectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('people/', views.PeopleView.as_view(), name='people'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('pharmacogenomics/', views.IndexView.as_view(), name='index2'),
    path('sider-searcher/', include('pharmacogenomics.urls')),
    path('pharmacogenomics/side-effect/', SideEffectView.as_view(), name='sider2'),
    path('gtexome/', include('gtexome.urls')),
]
