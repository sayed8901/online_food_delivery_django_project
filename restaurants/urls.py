from django.urls import path
from .views import (
    RestaurantListCreateView, RestaurantDetailView, MenuItemListCreateView, MenuItemDetailView,
    OrderCreateView, OrderListView, OwnerOrderListView, UpdateOrderStatusView
)



urlpatterns = [
    # owner only urls
    path('', RestaurantListCreateView.as_view(), name='restaurant-list'),
    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),

    path('menu/', MenuItemListCreateView.as_view(), name='menu-list'),
    path('menu/<int:pk>/', MenuItemDetailView.as_view(), name='menu-detail'),

    # user only urls
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),

    # owner only urls
    path('owner/orders/', OwnerOrderListView.as_view(), name='owner-orders'),
    path('owner/orders/<int:pk>/', UpdateOrderStatusView.as_view(), name='update-order-status'),
]
