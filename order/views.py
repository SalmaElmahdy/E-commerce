import datetime
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from cart.models import Cart_Item
from order.forms import OrderForm
from order.models import Order, OrderProduct, Payment
import uuid

from store.models import Product

def order_complete(request):
    order_number=request.GET.get('order_number')
    payment_id=request.GET.get('payment_id')
    
    try:
        
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        order_products=OrderProduct.objects.filter(order_id=order.pk)
        payment=Payment.objects.get(id=payment_id)
        sub_total=0
        for i in order_products:
            sub_total += i.product_price* i.quantity
        context={
            'order':order,
            'order_products':order_products,
            'payment_id':payment_id,
            'payment':payment,
            'sub_total':sub_total
        }
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
        
    return render(request,'order/order_complete.html',context)


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


def payment(request,order_number):
   # payment data
    order=Order.objects.filter(user=request.user,is_ordered=False,order_number=order_number)
    if order.exists():
        order=Order.objects.filter(user=request.user,is_ordered=False,order_number=order_number).first()
        order.is_ordered=True
        order.save()
        
        payment=_add_payment(request,order)
        _move_cart_to_order(request,order,payment)
        _reduce_quantity_of_products(request)
        _clear_cart(request)
        _send_order_recive_email(request,order)
    

        return redirect('/order/order_complete/?order_number='+str(order.order_number)+'&payment_id='+str(payment.pk))
    else:
        return HttpResponse('Not work:order not exist')

def _clear_cart(request):
    Cart_Item.objects.filter(user=request.user).delete()

def _reduce_quantity_of_products(request):
    cart_items=Cart_Item.objects.filter(user=request.user)
    for item in cart_items:
        product=Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    
def _add_payment(request,order):
    payment=Payment()
    payment.user=request.user
    
    namespace = uuid.UUID('00000000-0000-0000-0000-000000000000')  # Example namespace UUID
    name = 'example'

    uuid_value = uuid.uuid3(namespace, name)
    uuid_string = str(uuid_value).replace('-', '')

    payment.payment_id=uuid_string
    payment.payment_methos='paypal'
    payment.amount_paid=order.order_total
    payment.status='accept'
    payment.save()
   
    return payment


def _move_cart_to_order(request,order,payment):
    cart_items=Cart_Item.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order=order
        orderproduct.payment=payment
        orderproduct.user=request.user
        orderproduct.product=item.product
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.ordered=True
        orderproduct.save()
        
        # add variations of that item
        orderproduct.variations.set(_get_item_variation(item))  
        orderproduct.save()
        

def _get_item_variation(item):
    cart_item=Cart_Item.objects.get(id=item.id)
    product_variation=cart_item.variations.all()
    return product_variation
    
def _send_order_recive_email(request,order):
    mail_subject='Thank you for your order'
    message= render_to_string('mails/order_recieved_mail.html',{
        'user':request.user,
        'order':order
    })
    to_email=request.user.email
    send_email=EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()
    