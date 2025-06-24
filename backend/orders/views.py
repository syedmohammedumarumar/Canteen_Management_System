from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from .models import Order
from .serializers import OrderSerializer
from menu.models import MenuItem

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        menu_item = serializer.validated_data['menu_item']
        quantity = serializer.validated_data['quantity']

        if not menu_item.available or menu_item.stock < quantity:
            raise serializers.ValidationError("Item not available or stock too low.")

        menu_item.stock -= quantity
        menu_item.save()
        serializer.save(user=self.request.user)

class CancelOrderView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status='PLACED')

    def perform_update(self, serializer):
        order = self.get_object()
        order.status = 'CANCELLED'
        order.menu_item.stock += order.quantity
        order.menu_item.save()
        order.save()