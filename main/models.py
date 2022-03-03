from django.db import models
from django.conf import settings
from uuid import uuid4 
# Create your models here.
class Category(models.Model):
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag
    
    class Meta:
        verbose_name_plural = "categories"

class Food(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    prepareTime = models.DecimalField(max_digits=5, decimal_places=2)
    featured = models.BooleanField(default=False)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ("Pending","Pending"),
        ("Ordered","Ordered"),
        ("Prepared","Prepared"),
        ("Delivered","Delivered"),
        ("Cancelled","Cancelled"),  
    )
    transaction_id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_ordered = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending", choices=STATUS)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return f'{self.customer.username} || {self.transaction_id}'

    class Meta:
        ordering = ['-date_ordered']
    

class OrderItem(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.food.price * self.quantity
        return total

    def __str__(self):
        return f"{self.food} || {self.quantity}"


class Delivery(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.address}"


