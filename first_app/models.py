
from django.db import models
from django.conf import settings


class FoodItem(models.Model):
    CATEGORY_CHOICES = [
        ('Fast Food', 'Fast Food'),
        ('Main Course', 'Main Course'),
        ('Beverages', 'Beverages'),
        ('Desserts', 'Desserts'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name



class FoodCustomization(models.Model):
    GROUP_TYPE_CHOICES = [
        ('single', 'Single Select'),
        ('multiple', 'Multiple Select'),
    ]

    food_item = models.ForeignKey(
        FoodItem,
        on_delete=models.CASCADE,
        related_name='customization_options'
    )

    name = models.CharField(max_length=100)

    group_name = models.CharField(max_length=50, default='Extras')

    selection_type = models.CharField(
        max_length=10,
        choices=GROUP_TYPE_CHOICES,
        default='multiple'
    )

    is_required = models.BooleanField(default=False)

    additional_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('food_item', 'name')

    def __str__(self):
        return f"{self.food_item.name} - {self.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='orders'
)

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    food_item = models.ForeignKey(
        FoodItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    item_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    selected_customizations = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class TableBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    guests = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    special_request = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date}"
