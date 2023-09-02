import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render

from cart.models import Cart_Item
from order.forms import OrderForm
from order.models import Order

# Create your views here.
def payment(request):
    return render(request,'order/payment.html')
def place_order(request,total=0,quantity=0):
    cart_items=Cart_Item.objects.filter(user=request.user)
    if cart_items.count() <= 0:
        return redirect('store')
    
    grant_total=0
    tax=0
    for item in cart_items:
        total+=(item.product.price * item.quantity)
        quantity+=item.quantity
        
    tax=(2*total)/100
    grant_total=total+tax

    if request.method == 'POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.user=request.user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.counter=form.cleaned_data['counter']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grant_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime("%Y%m%d")
            order_number=current_date+str(data.id)
            data.order_number=order_number
            data.save()
            
            order=Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
            context={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grant_total':grant_total,
            }
            return render(request,'order/payment.html',context)
        else:
            return HttpResponse('form not valid')
            
    return redirect('checkout')