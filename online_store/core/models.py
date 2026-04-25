from django.db import models
from users.models import seller, customer

class product(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    seller = models.ForeignKey(to=seller, on_delete=models.CASCADE)
    inventory = models.IntegerField()
    def __str__(self):
        return self.name

class productImage(models.Model):
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(product, related_name='images', on_delete=models.CASCADE)


class order(models.Model):

    creation_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=30)
    customer = models.ForeignKey(to=customer, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(to=seller, on_delete=models.PROTECT)
    status = [('pending', 'pending'), ('completed', 'completed'), ('cancelled', 'cancelled')]
    order_status = models.CharField(max_length=9, choices=status, default='pending')
    total_value = models.DecimalField(max_digits=6, decimal_places=2)

class order_item(models.Model):
    product = models.ForeignKey(to=product, on_delete=models.PROTECT)
    quantity = models.SmallIntegerField()
    order = models.ForeignKey(to=order, on_delete=models.CASCADE)

class cart(models.Model):
    customer = models.OneToOneField(to=customer, on_delete=models.CASCADE)
    

class cart_item(models.Model):
    product = models.ForeignKey(to=product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    cart = models.ForeignKey(to=cart, on_delete=models.CASCADE)