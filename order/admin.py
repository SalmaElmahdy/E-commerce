from django.contrib import admin

from order.models import Order, OrderProduct, Payment

# Register your models here.
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(OrderProduct)