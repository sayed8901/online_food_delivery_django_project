from django.db import models
from orders.models import Order


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")  

    tran_id = models.CharField(max_length=100, unique=True)  # SSLCommerz transaction ID
    val_id = models.CharField(max_length=100, null=True, blank=True)  

    amount = models.DecimalField(max_digits=10, decimal_places=2)  
    currency = models.CharField(max_length=10, default="BDT")  

    card_type = models.CharField(max_length=50)
    card_brand = models.CharField(max_length=50, blank=True, null=True)
    bank_tran_id = models.CharField(max_length=100, blank=True, null=True)

    store_id = models.CharField(max_length=100)
    verify_sign = models.CharField(max_length=255)

    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Cancelled', 'Cancelled')
    ], default='Pending')

    tran_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.status}"
