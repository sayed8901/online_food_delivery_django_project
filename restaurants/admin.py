from django.contrib import admin
from .models import Restaurant, MenuItem



class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'location', 'description')

    search_fields = ('name', 'location', 'owner__username')
    list_filter = ('location', 'owner')



class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'restaurant', 'price', 'available')

    search_fields = ('name', 'restaurant__name')
    list_filter = ('available', 'restaurant')




admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
