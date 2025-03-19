from rest_framework import generics, permissions
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .models import Restaurant, MenuItem, Order, OrderItem
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






# Order Placement (User Only)
class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]

    def create(self, request, *args, **kwargs):
        user = request.user
        items_data = request.data.get('items', [])  # Extract items list from request
        restaurant_id = request.data.get('restaurant')  # Get restaurant ID

        # Validate restaurant
        try:
            restaurant = Restaurant.objects.get(id = restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found."}, status=status.HTTP_400_BAD_REQUEST)

        total_cost = 0
        order_items  = []

        # Ensure all items belong to the selected restaurant (each data has 'item' and 'quantity' fields)
        for item_data in items_data:
            item_id = item_data.get('item_id')
            quantity = item_data.get('quantity', 1)  # Default quantity to 1 if not provided

            try:
                menu_item = MenuItem.objects.get(
                    id = item_id, restaurant = restaurant, available=True
                )
            except MenuItem.DoesNotExist:
                return Response({"error": f"MenuItem ID {item_id} does not exist or is unavailable in this restaurant."}, status=status.HTTP_400_BAD_REQUEST)

            total_cost += (menu_item.price * quantity)  # Calculate total cost

            order_items.append((menu_item, quantity))   # Add to order_items list


        # Creating order
        order = Order.objects.create(
            user = user, restaurant = restaurant, total_cost = total_cost
        )

        # Create OrderItem objects to store item quantities
        for menu_item, quantity in order_items:
            OrderItem.objects.create(
                order = order, menu_item = menu_item, quantity = quantity
            )


        # Serialize and return the created order
        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)




# Order Tracking (User Only)
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user).order_by('-created_at')






# Order Management (Owner Only)
class OwnerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Order.objects.filter(restaurant__owner = self.request.user)




class UpdateOrderStatusView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


    def get_queryset(self):
        return Order.objects.filter(restaurant__owner = self.request.user)


    def update(self, request, *args, **kwargs):
        order = self.get_object()

        # Check if the order is paid before updating the status
        if not order.paid:
            return Response({"error": "Order has not been paid yet, cannot confirm."}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with the status update if the order is paid
        return super().update(request, *args, **kwargs)



