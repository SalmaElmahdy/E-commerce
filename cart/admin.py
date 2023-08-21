from django.contrib import admin

from .models import Cart, Cart_Item

class CartAdmin(admin.ModelAdmin):
    list_display=('cart_id','created_at')
    
class CartItemAdmin(admin.ModelAdmin):
    list_display=('product','cart','quantity','is_active')
# Register your models here.
admin.site.register(Cart,CartAdmin)
admin.site.register(Cart_Item,CartItemAdmin)