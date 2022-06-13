from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexListView.as_view(), name='index')
]