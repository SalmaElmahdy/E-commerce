from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart, Cart_Item
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Variation
from django.db.models import Count

# Create your views here.
def cart(request,total=0,quantity=0,cart_items=None):
    grant_total=0
    tax=0
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=Cart_Item.objects.filter(cart=cart,is_active=True)
        for item in cart_items:
            total+=(item.product.price * item.quantity)
            quantity+=item.quantity
        tax=(2*total)/100
        grant_total=total+tax
    except ObjectDoesNotExist:
        pass # just ignore
    
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grant_total':grant_total,
    }
    return render(request,'store/cart.html',context)

def add_to_cart(request,product_id):
    product= Product.objects.get(id=product_id)
    product_variation=_product_variation(request,product)
   
    cart=_get_cart(request)
    _add_product_to_cart(product,cart,product_variation)
    return redirect('cart')
        
def remove_cart(request,product_id,cart_item_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    
    try:
        cart_item=Cart_Item.objects.get(product=product,cart=cart,id= cart_item_id)
        if(cart_item.quantity>1):
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request,product_id,cart_item_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=Cart_Item.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


# make private function to get cart id
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def _get_cart(request):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    return cart

def _add_product_to_cart(product,cart,product_variation):
    
    is_cart_item_exists=Cart_Item.objects.filter(
            product=product,
            cart=cart,
        ).exists()
    
    if is_cart_item_exists:
        _create_or_update_item(product,cart,product_variation)
    else:
       _create_cart_item(product,product_variation)
   
def _create_or_update_item(product,cart,product_variation):
    cart_item=Cart_Item.objects.filter(product=product,cart=cart)
    ex_var_list=[]
    id=[]
    for item in cart_item:
        existing_variation= item.variations.all()
        ex_var_list.append(list(existing_variation))
        id.append(item.id)
    if product_variation in ex_var_list:
        index=ex_var_list.index(product_variation)
        item_id=id[index]
        item=Cart_Item.objects.get(product=product, id=item_id )
        item.quantity+=1
        item.save()
    else: 
        _create_cart_item(product,product_variation)

def _create_cart_item(product,product_variation):
    cart_item=Cart_Item.objects.create(
        product=product,
        quantity=1,
        cart=cart,
    )
        
    if len(product_variation) > 0 :
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
    cart_item.save()
    
    
    
def _product_variation(request,product):
    product_variation=[]
    if request.method=='POST':
        for param in request.POST:
            key=param
            value=request.POST[key]
            
            try:
                variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_values__iexact=value)
                product_variation.append(variation)
            except:
                pass
    return product_variation