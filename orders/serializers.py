from rest_framework import serializers
from .models import Restaurant, MenuItem, Order, OrderItem
from restaurants.serializers import MenuItemSerializer



# Serializer to show ordered items with their quantity
class OrderItemSerializer(serializers.ModelSerializer):
    # Extract only menu item name and description
    name = serializers.CharField(source='menu_item.name', read_only=True)  
    description = serializers.CharField(source='menu_item.description', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['name', 'description', 'quantity']  # Only return necessary fields




# Order Serializer (Handles Nested Order Items & Item Creation)
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(source='order_items.all', many=True, read_only=True)  # Show items with quantity
    
    items = serializers.ListField(write_only=True)  # Accepts a list of {item_id, quantity}

    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)  # Read-only field


    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'items', 'order_items', 'total_cost', 'status', 'created_at', 'is_payment_done',]


