from django.urls import path
from .views import (
    OrderCreateView, OrderListView, UserOrdersView,
    OwnerOrderListView, UpdateOrderStatusView
)



urlpatterns = [
    # Orders Placement API       # user only urls
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('all/', OrderListView.as_view(), name='order-list'),
    path('user/<int:user_id>/', UserOrdersView.as_view(), name='user-orders'),

    # Orders list_view API       # owner only urls
    path('owner/', OwnerOrderListView.as_view(), name='owner-orders'),
    path('owner/update/<int:pk>/', UpdateOrderStatusView.as_view(), name='update-order-status'),
]

