from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
    ]

    LOW_STOCK_THRESHOLD = 5

    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.sku})"

    # ---- Business rules as model properties ----

    @property
    def is_low_stock(self):
        """Stock of 5 or below (but not zero-negative cases) counts as low stock."""
        return 0 < self.stock <= self.LOW_STOCK_THRESHOLD

    @property
    def is_out_of_stock(self):
        return self.stock == 0

    # ---- Database-level validation ----

    def clean(self):
        if self.price is not None and self.price <= 0:
            raise ValidationError({'price': 'Price must be greater than 0.'})
        if self.stock is None or self.stock < 0:
            raise ValidationError({'stock': 'Stock cannot be negative.'})