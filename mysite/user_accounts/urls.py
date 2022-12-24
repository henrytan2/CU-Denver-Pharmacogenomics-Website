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
from .views import profile, contact
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    # path(r'templates/users', profile, name='users-profile'),
    # path(r'profile/', profile, name='users-profile'),
    path(r'templates/login', views.contact, name='login'),
    path(r'templates/profile', contact, name='profile'),
    path('admin/', admin.site.urls),
    # path('api/accounts/', include('authemail.urls')),

    path('signup/', views.Signup.as_view(), name='authemail-signup'),
    path('signup/verify/', views.SignupVerify.as_view(),
         name='authemail-signup-verify'),

    path('login/', views.Login.as_view(), name='authemail-login'),
    path('logout/', views.Logout.as_view(), name='authemail-logout'),

    path('password/reset/', views.PasswordReset.as_view(),
         name='authemail-password-reset'),
    path('password/reset/verify/', views.PasswordResetVerify.as_view(),
         name='authemail-password-reset-verify'),
    path('password/reset/verified/', views.PasswordResetVerified.as_view(),
         name='authemail-password-reset-verified'),

    path('email/change/', views.EmailChange.as_view(),
         name='authemail-email-change'),
    path('email/change/verify/', views.EmailChangeVerify.as_view(),
         name='authemail-email-change-verify'),

    path('password/change/', views.PasswordChange.as_view(),
         name='authemail-password-change'),

    path('users/me/', views.UserMe.as_view(), name='authemail-me'),
]


urlpatterns = format_suffix_patterns(urlpatterns)