from django.contrib import admin

from .models import Product, ReviewRating, Variation

# populate the slug
class ProductAdmin(admin.ModelAdmin):
    # we add comma to know it is tuple field
    prepopulated_fields={'slug':('product_name',)}
    list_display=('product_name','price','stock','category','updated_at','is_available')

class VariationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_values','is_active')
    list_editable=('is_active',)
    list_filter=('product','variation_category','variation_values')
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating)