from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from cart.models import Cart_Item
from cart.views import _cart_id
from category.models import Category
from django.core.paginator import Paginator
from store.models import Product
from django.db.models import Q

# Create your views here.
def store(request,category_slug=None):
    categories=None
    products=None
    if category_slug !=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)
    else:
        products=Product.objects.filter(is_available=True)
        
    # apply paginator on result data but the data should be ordered bc it gives me warning  
    paginator=Paginator(products.order_by('id'),2)
    # get page number from url as its write [/?page=2]
    page=request.GET.get('page')
    # get product in specific page number
    paged_products=paginator.get_page(page)
    product_count=products.count()
    context={
        'products':paged_products,
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


def search(request):
    if('keyword' in request.GET):
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('-created_at').filter(Q(description__icontains=keyword) | Q( product_name__icontains = keyword))
        else:
            products=Product.objects.order_by('-created_at')
        
        product_count=products.count()
        context={
                'products':products,
                'product_count':product_count
            }
    return render(request,'store/store.html',context)