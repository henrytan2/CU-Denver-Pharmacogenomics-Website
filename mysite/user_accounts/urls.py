from django.urls import path
from . import views

app_name = 'user_accounts'

urlpatterns = [
    path('api-token', views.GetAPITokenView.as_view(), name='get-api-token'),
    path('send-reset-email', views.send_reset_email, name='send-reset-email'),
    path('sign-up', views.sign_up, name='signup')
]
