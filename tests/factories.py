import factory
from category.models import Category
from store.models import Product, Variation
from factory import  SubFactory,Faker

####
# Category
###
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        
    category_name = "django"
    slug = "django"
    
    
####
# Product
###
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model= Product
        django_get_or_create = ('product_name','slug')
    
    product_name = 'shirt'
    slug = 'shirt'
    description = Faker('text')
    price = Faker('random_int', min=10, max=1000)
    images = Faker('image_url', width=200, height=200)
    stock = Faker('random_int', min=1, max=100)
    is_available = True
    category = SubFactory(CategoryFactory)
    
    # I used that for creation method if i wanted to handle exception of create
    # not unique values for product_name and slug but i handeled it with django_get_or_create
    # as it is not create the same object twice its just create one so no exception of uniqueness
    
    # @classmethod
    # def _create(cls, model_class, *args, **kwargs):
    #     """
    #     Override the default _create method to handle the unique fields.
    #     """
    #     return model_class.objects.create(*args, **kwargs)



####
# Variation
###
class VariationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Variation
        
    product = factory.SubFactory(ProductFactory)
    variation_category = factory.Iterator([choice[0] for choice in Variation.variation_category_choice])
    variation_values = factory.Faker('word')
    is_active = True
    
    
     
# In the provided factory code,
# the `@classmethod` decorator is used to define a method named `_create` inside the `ProductFactory` class.
# 
# Let's break down what this method does:

# ```python
# @classmethod
# def _create(cls, model_class, *args, **kwargs):
#     """
#     Override the default _create method to handle the unique fields.
#     """
#     return model_class.objects.create(*args, **kwargs)
# ```

# 1. `@classmethod`: This is a Python decorator used to indicate that the following method is a class method rather than an instance method. 
# Class methods receive the class itself as their first argument (`cls`) instead of an instance of the class.

# 2. `def _create(cls, model_class, *args, **kwargs)`: This is the method definition. It takes several arguments:

#    - `cls`: This is a reference to the class itself (in this case, `ProductFactory`).
   
#    - `model_class`: This is the class of the model for which an instance is being created (in this case, `Product`).
   
#    - `*args` and `**kwargs`: These are used to pass any additional positional or keyword arguments to the method.


# 3. `return model_class.objects.create(*args, **kwargs)`: 
# This is the actual code that creates an instance of the model (`Product`) using `model_class.objects.create`.

#    - `model_class.objects`: This accesses the manager for the model class. In this case, it's accessing the manager for the `Product` model.
   
#    - `.create(*args, **kwargs)`:
#       This is a method provided by Django's ORM for creating a new object of the model. 
#       It takes any additional arguments and keyword arguments (`*args` and `**kwargs`) and uses them to initialize the fields of the object.

#    - The resulting object is then returned.

# The purpose of this method is to handle cases where there are unique fields in the model, 
# such as `product_name` and `slug`. Since `Faker` might generate data that conflicts with existing records, 
# this method overrides the default behavior of the factory to ensure uniqueness.

# By using `model_class.objects.create`, 
# it ensures that the object is created in the database using Django's ORM, 
# which enforces the uniqueness constraints specified in the model. 
# This way, if a generated value is not unique, the ORM will raise an integrity error, 
# which can be caught and handled appropriately.