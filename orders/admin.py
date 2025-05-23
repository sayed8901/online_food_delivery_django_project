from django.contrib import admin
from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'display_items_with_quantity', 'total_cost', 'status', 'created_at', 'is_payment_done',)

    search_fields = ('user__username', 'restaurant__name')
    list_filter = ('status', 'restaurant', 'created_at')

    ordering = ('-created_at',)

    # Custom method to display ordered items with their quantities
    def display_items_with_quantity(self, obj):
        order_items = OrderItem.objects.filter(order = obj)  # Access the 'OrderItem' model
        print("order_items", order_items)
        
        items_list = [f"{order_item.menu_item.name} ({order_item.quantity} pcs)" for order_item in order_items]
        return ", ".join(items_list) if items_list else "No items ordered"

    display_items_with_quantity.short_description = "Ordered Items (with Quantity)"  # Column header in admin panel


admin.site.register(Order, OrderAdmin)
