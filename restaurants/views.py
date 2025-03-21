from rest_framework import generics, permissions
from rest_framework import serializers

from .models import Restaurant, MenuItem
from .serializers import RestaurantSerializer, MenuItemSerializer
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




# CRUD Operations for Menu Items
class MenuItemListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    # Handle GET operation (can retrieve by both user or owner)
    def get_queryset(self):
        user = self.request.user

        if user.role == 'owner':
            # returns only the menu items by filters for only this owner user, He will not able to see the other owners menu items
            return MenuItem.objects.filter(restaurant__owner = user) 
        else:
            return MenuItem.objects.all()  # Users can see all menu items


    # Handle POST operation (Owner Only)
    def perform_create(self, serializer):
        # Get restaurant ID from request's 'restaurant' field
        restaurant_id = self.request.data.get('restaurant')  

        try:
            # Assign the restaurant dynamically
            restaurant = Restaurant.objects.get(
                id = restaurant_id, owner = self.request.user
            )
            serializer.save(restaurant = restaurant)  

        except Restaurant.DoesNotExist:
            raise serializers.ValidationError("Invalid restaurant ID or you don't own this restaurant.")



# Handle ID-wise GET operation (can retrieve by both user or owner)
# Handle ID-wise PUT, PATCH & DELETE operation (Owner Only)
class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    queryset = MenuItem.objects.all()

