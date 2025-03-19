from django.db import models
from accounts.models import CustomUser


class Restaurant(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="restaurants")

    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)

    # image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)


    def __str__(self):
        return self.name



class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_items")

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)


    def __str__(self):
        return self.name



# Intermediary model to store quantity of each item in an order
class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="order_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Store quantity

    

class Order(models.Model):
    STATUS_CHOICES = [
        ('Preparing', 'Preparing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="orders")

    items = models.ManyToManyField(MenuItem)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Preparing')

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)


    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
