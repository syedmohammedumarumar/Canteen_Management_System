from django.urls import path
from .views import (OrderListCreateView, 
                    CancelOrderView ,
                    UpdateOrderStatusView,
                    DailyOrderSummaryView,
                    AdminOrderListView,
                    place_order)
urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('', OrderListCreateView.as_view(), name='orders'),
    path('admin/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('<int:pk>/update-status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('<int:pk>/cancel/', CancelOrderView.as_view(), name='cancel-order'),
    path('summary/today/', DailyOrderSummaryView.as_view(), name='daily-summary'),
]

