from rest_framework import serializers
from .models import Order
from menu.models import MenuItem

class OrderSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.ReadOnlyField(source='menu_item.name')

    class Meta:
        model = Order
        fields = ['id', 'user', 'menu_item', 'menu_item_name', 'quantity', 'timestamp', 'status']
        read_only_fields = ['user', 'timestamp', 'status']