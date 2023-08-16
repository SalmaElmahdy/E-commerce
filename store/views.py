from django.shortcuts import get_object_or_404, render
from cart.models import Cart_Item
from cart.views import _cart_id
from category.models import Category

from store.models import Product

# Create your views here.
def store(request,category_slug=None):
    categories=None
    products=None
    if category_slug !=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)
        product_count=products.count()
    else:
        products=Product.objects.filter(is_available=True)
        product_count=products.count()
    context={
        'products':products,
        'product_count':product_count
    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    
    # we use category__slug as it get category model and get slug in the category model
    try:
        product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=Cart_Item.objects.filter(cart__cart_id=_cart_id(request),product=product).exists()
    except Exception as e:
        raise e
    
    
    context={
        'product':product,
        'in_cart':in_cart
    }
    return render(request,'store/product_detail.html',context)