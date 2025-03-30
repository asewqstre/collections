from django.urls import path
from .views import create_collection_view, delete_collection_view

urlpatterns = [
    path('create/', create_collection_view, name='Create_collection'),
    path('<int:pk>/delete/', delete_collection_view, name='Delete_collection'),
    ]