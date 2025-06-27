from django.contrib import admin
from .models import Order, OrderItem

# Remove or comment out any previous `admin.site.register(Order)` above

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'timestamp']
    inlines = [OrderItemInline]  # Display OrderItems inline

# Register with updated admin config
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)