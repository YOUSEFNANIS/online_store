from django.db import models
from users.models import seller, customer
from django.conf import settings
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator

class Category(models.Model):
    slug = models.SlugField(unique=True)
    name_en = models.CharField(max_length=60)
    name_ar = models.CharField(max_length=60)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name_en

class product(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    seller = models.ForeignKey(to=seller, on_delete=models.CASCADE)
    inventory = models.IntegerField()
    category = models.ForeignKey(Category, null=True, blank=True, related_name='products', on_delete=models.SET_NULL)
    def __str__(self):
        return self.name

class productImage(models.Model):
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(product, related_name='images', on_delete=models.CASCADE)
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]

class order(models.Model):

    creation_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=30)
    customer = models.ForeignKey(to=customer, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(to=seller, on_delete=models.PROTECT)
    status = [('pending', 'pending'), ('confirmed', 'confirmed'), ('shipped', 'shipped'),
              ('delivered', 'delivered'), ('cancelled', 'cancelled')]
    order_status = models.CharField(max_length=9, choices=status, default='pending')
    total_value = models.DecimalField(max_digits=6, decimal_places=2)
    payment_method = models.CharField(max_length=3, choices=[('cod', 'cash on delivery')], default='cod')
    payment_status = models.CharField(max_length=6, choices=[('unpaid', 'unpaid'), ('paid', 'paid')], default='unpaid')

class OrderStatusEvent(models.Model):
    order = models.ForeignKey(order, related_name='events', on_delete=models.CASCADE)
    status = models.CharField(max_length=9)
    actor_role = models.CharField(max_length=8)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created', 'id']

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

class Review(models.Model):
    product = models.ForeignKey(product, related_name='reviews', on_delete=models.CASCADE)
    customer = models.ForeignKey(customer, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'customer')
        ordering = ['-created', '-id']

class Report(models.Model):
    reasons = [('spam', 'spam'), ('fraud', 'fraud'), ('inappropriate', 'inappropriate'),
               ('counterfeit', 'counterfeit'), ('other', 'other')]
    statuses = [('open', 'open'), ('resolved', 'resolved'), ('dismissed', 'dismissed')]
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reports', on_delete=models.CASCADE)
    product = models.ForeignKey(product, null=True, blank=True, related_name='reports', on_delete=models.CASCADE)
    seller = models.ForeignKey(seller, null=True, blank=True, related_name='reports', on_delete=models.CASCADE)
    reason = models.CharField(max_length=13, choices=reasons)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=9, choices=statuses, default='open')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', '-id']

class WishlistItem(models.Model):
    customer = models.ForeignKey(customer, related_name='wishlist', on_delete=models.CASCADE)
    product = models.ForeignKey(product, related_name='wishlisted_by', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'product')
        ordering = ['-created', '-id']

class Payout(models.Model):
    seller = models.ForeignKey(seller, related_name='payouts', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=7, choices=[('pending', 'pending'), ('paid', 'paid')], default='pending')
    created = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created', '-id']

class LedgerEntry(models.Model):
    kinds = [('sale', 'sale'), ('commission', 'commission'), ('payout', 'payout'), ('adjustment', 'adjustment')]
    seller = models.ForeignKey(seller, related_name='ledger', on_delete=models.PROTECT)
    kind = models.CharField(max_length=10, choices=kinds)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # signed: sales +, commission and payouts -
    order = models.ForeignKey(order, null=True, blank=True, related_name='ledger_entries', on_delete=models.SET_NULL)
    payout = models.ForeignKey(Payout, null=True, blank=True, related_name='ledger_entries', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', '-id']
