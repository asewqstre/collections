from django.urls import path
from .views import create_collection_view

urlpatterns = [
    path('create/', create_collection_view, name='Create_collection'),
]
