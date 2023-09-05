from django.contrib import admin

from order.models import Order, OrderProduct, Payment

class OrderProductInline(admin.TabularInline):
    model=OrderProduct
    # use extra te remove extra rows
    extra=0 
    readonly_fields=['payment','user','product','quantity','product_price','ordered']
    
class OrderAdmin(admin.ModelAdmin):
    list_display=['order_number','full_name','phone','email','city','order_total','tax','status','is_ordered','created_at']
    list_filter=['status','is_ordered']
    search_fields=['order_number','first_name','last_name','email','phone']
    list_per_page=20
    inlines=[OrderProductInline]
    
admin.site.register(Order,OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct)