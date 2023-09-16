from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from cart.models import Cart_Item
from cart.views import _cart_id
from category.models import Category
from django.core.paginator import Paginator
from decorators.decorators import is_purchase_product
from order.models import OrderProduct
from store.forms import ReviewForm
from store.models import Product, ReviewRating
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


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
        reviews=ReviewRating.objects.filter(product_id=product.id,status=True)
    except Exception as e:
        raise e
    
    
    context={
        'product':product,
        'in_cart':in_cart,
        'reviews':reviews
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


# if user need to submit review he should be 
# logged in and purchace that product
@login_required(login_url="login")
@is_purchase_product
def submit_review(request,product_id):
    url=request.META.get('HTTP_REFERER') # store the current url
    if request.method=='POST':
        try:
            reviews= ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            # we pass the instance so when already there is review then update it
            # so that create or update
            form = ReviewForm(request.POST,instance=reviews)
            form.save()
      
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data= ReviewRating()
                data.subject=form.cleaned_data['subject']
                data.rating=form.cleaned_data['rating']
                data.review=form.cleaned_data['review']
                data.ip=request.META.get('REMOTE_ADDR')
                data.product_id=product_id
                data.user_id=request.user.id
                data.save()
            
        messages.success(request,"Thank You! Your review has been submited.")
        return redirect(url)

