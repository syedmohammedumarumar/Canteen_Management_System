from django.urls import path
from .views import OrderListCreateView, CancelOrderView

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('', OrderListCreateView.as_view(), name='orders'),
    path('<int:pk>/cancel/', CancelOrderView.as_view(), name='cancel-order'),
]
