from order.models import OrderProduct
from django.contrib import messages
from django.shortcuts import redirect

def is_purchase_product(func):
    def inner(request,product_id):
        orderProduct=OrderProduct.objects.filter(user=request.user,product_id=product_id)
        if orderProduct.exists():
            return func(request,product_id)
        else:
            messages.error(request,"You must By the product first")
            return redirect(request.META.get('HTTP_REFERER')) 
    return inner