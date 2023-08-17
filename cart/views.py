from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart, Cart_Item
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product

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
    cart=_get_cart(request)
    _add_product_to_cart(product,cart)
    return redirect('cart')
        
def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=Cart_Item.objects.get(product=product,cart=cart)
    if(cart_item.quantity>1):
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=Cart_Item.objects.get(product=product,cart=cart)
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

def _add_product_to_cart(product,cart):
    try:
        cart_item=Cart_Item.objects.get(product=product,cart=cart)
        cart_item.quantity +=1
        cart_item.save()
    except Cart_Item.DoesNotExist:
        cart_item=Cart_Item.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
    cart_item.save()