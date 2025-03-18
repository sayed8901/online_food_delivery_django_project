from rest_framework import generics, permissions
from .models import Restaurant, MenuItem, Order
from .serializers import RestaurantSerializer, MenuItemSerializer, OrderSerializer
from accounts.permissions import IsOwner, IsUser, IsOwnerOrReadOnly



# CRUD Operations for Restaurants (Owner Only)
class RestaurantListCreateView(generics.ListCreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    # Handle GET operation
    def get_queryset(self):
        return Restaurant.objects.all()

    # Handle POST operation
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Handle ID-wise GET, PUT, PATCH & DELETE operation
class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    queryset = Restaurant.objects.all()




# CRUD Operations for Menu Items (Owner Only)
class MenuItemListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    # Handle GET operation (can retrieve both user or owner)
    def get_queryset(self):
        return MenuItem.objects.filter(restaurant__owner=self.request.user)

    # Handle POST operation (Owner Only)
    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.restaurants.first())  # Auto-link to owner's restaurant



# Handle ID-wise GET operation (can retrieve both user or owner)
# Handle ID-wise PUT, PATCH & DELETE operation (Owner Only)
class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    queryset = MenuItem.objects.all()






# Order Placement (User Only)
class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




# Order Tracking (User Only)
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)






# Order Management (Owner Only)
class OwnerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Order.objects.filter(restaurant__owner=self.request.user)


class UpdateOrderStatusView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Order.objects.filter(restaurant__owner=self.request.user)

