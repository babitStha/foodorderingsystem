from django.contrib import admin
from . models import Category,Food,OrderItem, Order

# Register your models here.
admin.site.site_header="Food Ordering System Admin"
admin.site.register(Category)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(OrderItem)