from django.db import models
from django.urls import reverse

from category.models import Category

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug= models.SlugField(max_length=200,unique=True)
    description=models.TextField(max_length=500,blank=True)
    price=models.IntegerField()
    images=models.ImageField(upload_to='photos/products')
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    # when delete category delete all products with that category
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_name
    
    # get details for single product
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
    



class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)
    
class Variation(models.Model):
    variation_category_choice=[
    ('color','color'),
    ('size','size'),
    ]
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_choice)
    variation_values=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    objects=VariationManager()
    
    def __str__(self):
        return self.variation_values


# In Django, a "manager" is a class that provides a high-level interface for interacting with the database.
# Every Django model has at least one manager, which is used to perform various database operations
# such as creating, querying, updating, and deleting records.

# By default, Django provides a manager for every model called `objects`. 
# This manager gives you access to standard database operations.

# However, in the code you provided, a custom manager named `VariationManager` is defined:

# ```python
# class VariationManager(models.Manager):
#     def colors(self):
#         return super(VariationManager, self).filter(variation_category='color', is_active=True)

#     def sizes(self):
#         return super(VariationManager, self).filter(variation_category='size', is_active=True)
# ```

# This custom manager, `VariationManager`, extends the default manager (`models.Manager`)
# and provides two custom methods: `colors()` and `sizes()`.
# These methods perform specialized queries on the `Variation` model.

# 1. `colors(self)`: This method returns a queryset of `Variation` objects where `variation_category` is set to 'color' and `is_active` is `True`.

# 2. `sizes(self)`: This method returns a queryset of `Variation` objects where `variation_category` is set to 'size' and `is_active` is `True`.

# Now, this custom manager is associated with the `Variation` model using:

# ```python
# objects = VariationManager()
# ```

# This line means that any instance of the `Variation` model will use the `VariationManager` as its default manager,
# instead of the default `objects` manager provided by Django.

# So, when you have a `Variation` object, you can use the custom methods 
# `colors()` and `sizes()` to easily query for variations of a specific category. 
# 
# For example:

# ```python
# # Query for all color variations
# color_variations = Variation.objects.colors()

# # Query for all size variations
# size_variations = Variation.objects.sizes()
# ```

# This allows for more specialized and convenient querying of `Variation` objects based on their category.