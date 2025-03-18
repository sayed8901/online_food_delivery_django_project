from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    def username(self, obj):
        return obj.user.username
    
    def first_name(self, obj):
        return obj.user.first_name
    
    def last_name(self, obj):
        return obj.user.last_name
    
    def email(self, obj):
        return obj.user.email
    
    def role(self, obj):
        return obj.user.role
    
    def is_active(self, obj):
        return obj.user.is_active
    
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'is_active',]


admin.site.register(CustomUser, CustomUserAdmin)