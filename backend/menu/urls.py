from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_items, name='list-items'),
    path('add/', views.add_item, name='add-item'),
    path('<int:pk>/update/', views.update_item, name='update-item'),
    path('<int:pk>/delete/', views.delete_item, name='delete-item'),
]