from django.urls import path
from .views import (
    OrderCreateView, OrderListView, 
    OwnerOrderListView, UpdateOrderStatusView
)



urlpatterns = [
    # Orders Placement API       # user only urls
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),


    # Orders list_view API       # owner only urls
    path('owner/orders/', OwnerOrderListView.as_view(), name='owner-orders'),
    path('owner/orders/<int:pk>/', UpdateOrderStatusView.as_view(), name='update-order-status'),
]

