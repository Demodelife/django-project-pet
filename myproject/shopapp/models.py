from django.contrib.auth.models import User
from django.db import models


def image_path_upload(instance: 'ProductImage', filename: str) -> str:
    return f'products/product_{instance.product.pk}/images/{filename}'


def preview_path_upload(instance: 'Product', filename: str) -> str:
    return f'products/product_{instance.pk}/preview/{filename}'


class Product(models.Model):
    """
    Model Product.

    Orders here: :model:`shopapp.Order`
    """
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=preview_path_upload)


class ProductImage(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_path_upload)


class Order(models.Model):
    """Model Order"""
    delivery_address = models.CharField(max_length=100, null=False, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='orders')
