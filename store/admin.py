from django.contrib import admin

from .models import Product

# populate the slug
class ProductAdmin(admin.ModelAdmin):
    # we add comma to know it is tuple field
    prepopulated_fields={'slug':('product_name',)}
    list_display=('product_name','price','stock','category','updated_at','is_available')
    
admin.site.register(Product, ProductAdmin)