from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status

from .models import Restaurant, MenuItem, Order, OrderItem
from .serializers import OrderSerializer
from accounts.permissions import IsOwner, IsUser, IsOwnerOrReadOnly



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

