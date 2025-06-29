from rest_framework import generics, permissions, serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.timezone import now
from django.http import JsonResponse
from django.core.mail import send_mail
from django.db.models import Sum, Count

from .models import Order, OrderItem
from .serializers import OrderSerializer
from menu.models import MenuItem
from menu.serializers import MenuItemSerializer  


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'menu_item', 'timestamp']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()  
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        menu_item = serializer.validated_data['menu_item']
        quantity = serializer.validated_data['quantity']

        
        if not menu_item.available:
            raise serializers.ValidationError("Item not available.")
        
        order = serializer.save(user=self.request.user)

       
        send_mail(
            subject='Order Confirmation',
            message=f"Thank you! Your order for {menu_item.name} x {quantity} has been placed.",
            from_email=None,
            recipient_list=[self.request.user.email],
            fail_silently=True
        )

class MenuItemListView(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'available']


class CancelOrderView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status='PLACED')

    def perform_update(self, serializer):
        order = self.get_object()
        order.status = 'CANCELLED'
       
        order.save()

class UpdateOrderStatusView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()


class DailyOrderSummaryView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = now().date()
        orders_today = Order.objects.filter(timestamp__date=today)
        total_orders = orders_today.count()
        total_quantity = orders_today.aggregate(Sum('quantity'))['quantity__sum'] or 0
        items_breakdown = orders_today.values('menu_item__name').annotate(total=Count('menu_item'))

        return JsonResponse({
            "date": str(today),
            "total_orders": total_orders,
            "total_quantity": total_quantity,
            "items_summary": list(items_breakdown),
        })

class AdminOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()  