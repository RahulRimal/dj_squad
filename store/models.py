from django.db import models
# from django.db.models import Model, CharField
# Create your models here.

from django.contrib.auth.models import User

from uuid import uuid4


class Collection(models.Model):
    name = models.CharField(max_length=100)
    featured_product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, blank=True, null=True, related_name="+")

    def __str__(self):
        return self.name.capitalize()


class Product(models.Model):
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    inventory = models.PositiveIntegerField()
    description = models.TextField()
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)

    def __str__(self):
        return self.name.capitalize()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="images/store/products", null=True, blank=True)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


ORDER_STATUS_PENDING = "p"
ORDER_STATUS_COMPLETE = "c"
ORDER_STATUS_FAILED = "f"

ORDER_STATUS_CHOICES = [
    (ORDER_STATUS_PENDING, "Pending"),
    (ORDER_STATUS_COMPLETE, "Complete"),
    (ORDER_STATUS_FAILED, "Failed"),
]


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    placed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1, default=ORDER_STATUS_PENDING,
        choices=ORDER_STATUS_CHOICES)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
