from rest_framework import generics, permissions
from rest_framework import serializers

from .models import Restaurant, MenuItem
from .serializers import RestaurantSerializer, MenuItemSerializer
from accounts.permissions import IsOwner, IsUser, IsOwnerOrReadOnly

from drf_spectacular.utils import extend_schema





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
class AllRestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    queryset = Restaurant.objects.all()




# To Get Menu Items for a Specific Restaurant
class RestaurantMenuItemsView(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return MenuItem.objects.filter(restaurant__id = restaurant_id)
    




# CRUD Operations for Menu Items
class MenuItemListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    # Handle GET operation (can retrieve by both user or owner)
    def get_queryset(self):
        user = self.request.user

        if user.role == 'owner':
            # returns only the menu items by filters for only this owner user, He will not able to see the other owners menu items
            return MenuItem.objects.filter(restaurant = user.restaurant) 
        else:
            return MenuItem.objects.all()  # Users can see all menu items


    # Handle POST operation (Owner Only)
    def perform_create(self, serializer):
        user = self.request.user

        if user.role != 'owner':
            raise serializers.ValidationError("Only restaurant owners can add menu items.")

        try:
            restaurant = user.restaurant  # Auto-fetch the restaurant using OneToOneField
        except ObjectDoesNotExist:
            raise serializers.ValidationError("You don't have a registered restaurant.")

        serializer.save(restaurant=restaurant)  # Automatically set restaurant



    @extend_schema(operation_id="list_all_menu_items")
    def get(self, request, *args, **kwargs):
        """Retrieve all menu items from all restaurants."""
        return super().get(request, *args, **kwargs)
    




# Handle ID-wise GET operation (can retrieve by both user or owner)
# Handle ID-wise PUT, PATCH & DELETE operation (Owner Only)
class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    queryset = MenuItem.objects.all()


