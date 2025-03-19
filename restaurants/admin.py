from django.contrib import admin
from .models import Restaurant, MenuItem, Order, OrderItem



class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'location', 'description')

    search_fields = ('name', 'location', 'owner__username')
    list_filter = ('location', 'owner')



class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'restaurant', 'price', 'available')

    search_fields = ('name', 'restaurant__name')
    list_filter = ('available', 'restaurant')



class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'display_items_with_quantity', 'total_cost', 'status', 'created_at', 'paid',)

    search_fields = ('user__username', 'restaurant__name')
    list_filter = ('status', 'restaurant', 'created_at')

    ordering = ('-created_at',)


    # Custom method to display ordered items with their quantities
    def display_items_with_quantity(self, obj):
        order_items = OrderItem.objects.filter(order = obj)  # Access the 'OrderItem' model
        print("order_items", order_items)
        
        items_list = [f"{order_item.menu_item.name} (qty: {order_item.quantity})" for order_item in order_items]
        return ", ".join(items_list) if items_list else "No items ordered"

    display_items_with_quantity.short_description = "Ordered Items (with Quantity)"  # Column header in admin panel




admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
