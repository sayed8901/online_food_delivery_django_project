from django.contrib import admin
from .models import Restaurant, MenuItem, Order


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'location', 'description')
    search_fields = ('name', 'location', 'owner__username')
    list_filter = ('location', 'owner')

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'restaurant', 'price', 'available')
    search_fields = ('name', 'restaurant__name')
    list_filter = ('available', 'restaurant')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'total_cost', 'status', 'created_at')
    search_fields = ('user__username', 'restaurant__name')
    list_filter = ('status', 'restaurant', 'created_at')
    ordering = ('-created_at',)


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
