from django.urls import path, include
from .views import EsnuelOutputInsertView, EsnuelOutputFetchView

app_name = 'esnuel'

urlpatterns = [
    path(r'/insert', EsnuelOutputInsertView.as_view(), name='esnuel_insert'),
    path('/fetch', EsnuelOutputFetchView.as_view(), name='esnuel_fetch'),
]