from django.urls import path
from .views import (
    RestaurantListCreateView, AllRestaurantDetailView, RestaurantMenuItemsView, 
    MenuItemListCreateView, MenuItemDetailView
)



urlpatterns = [
    # Restaurants API           # owner only urls
    path('', RestaurantListCreateView.as_view(), name='restaurant-list'),
    path('<int:pk>/', AllRestaurantDetailView.as_view(), name='restaurant-detail'),


    # Menu Items API       
    path('menu/', MenuItemListCreateView.as_view(), name='menu-list'),
    path('menu/<int:pk>/', MenuItemDetailView.as_view(), name='menu-detail'),


    # New Endpoint to Get Menu Items by Restaurant
    path('<int:restaurant_id>/menu/', RestaurantMenuItemsView.as_view(), name='restaurant-menu-items'),
]


