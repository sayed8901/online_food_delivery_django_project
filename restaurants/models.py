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


