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

def passwords_match_validator(func):
    def inner(request,*args,**kwargs):
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Password and confirm password do not match.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        return func(request, *args, **kwargs)
    
    return inner