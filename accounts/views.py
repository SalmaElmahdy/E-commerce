from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.forms import RegisterationForm, UserForm, UserProfileForm
from accounts.models import Account, UserProfile
from decorators.decorators import passwords_match_validator
from order.models import Order, OrderProduct
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

# verfication email
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

from cart.models import Cart, Cart_Item
from cart.views import _cart_id
import requests

import threading

class HandleAcitvationMail(threading.Thread):
    def __init__(self,request,user):
        self.request=request
        self.user=user
        
        threading.Thread.__init__(self)
    
    def run(self):
        current_site=get_current_site(self.request)
        mail_subject='Please activate your account'
        message= render_to_string('mails/account_verification_email.html',{
            'user':self.user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token':default_token_generator.make_token(self.user),
        })
        to_email=self.user.email
        send_email=EmailMessage(mail_subject,message,to=[to_email])
        send_email.send()

@login_required(login_url="login")
@passwords_match_validator
def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['password']
        user = Account.objects.get(username__exact=request.user.username)
        user.set_password(new_password)
        user.save()
        messages.success(request,"Password updated successfully.")
        return redirect('change_password')
    return render(request,'accounts/change_password.html')
    

@login_required(login_url="login")
def order_detail(request,order_id):
    order_detail=OrderProduct.objects.filter(order__order_number=order_id)
    order=Order.objects.get(order_number=order_id)
    sub_total=0
    for i in order_detail:
        sub_total += i.product_price* i.quantity
    context={
        'order_detail':order_detail,
        'order':order,
        'sub_total':sub_total
    }
    
    return render(request,'accounts/order_detail.html',context)  
    
def edit_profile(request):
    userProfile=get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=request.user)
        profile_form=UserProfileForm(request.POST,request.FILES,instance=userProfile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form= UserProfileForm(instance=userProfile)
        
    context={
        'user_form':user_form,
        'profile_form':profile_form,
        'user_profile':userProfile
    }
    return render(request,'accounts/edit_profile.html',context)

# Create your views here.
@passwords_match_validator
def register(request):
    if request.method =='POST':
        form =RegisterationForm(request.POST)
        if form.is_valid():
            user= _create_user(form)
            _add_user_profile_data(user)
            # _send_user_activation_mail(request,user)
            HandleAcitvationMail(request,user).start()
            # used threads to improve performance of request
            # messages.success(request, "Thanks for registering with us. We have send you a verification email to {{user.email}}, Please verify it")
            return redirect('/account/login/?command=verification&email='+user.email)
        else:
            messages.error(request,form['email'].errors)
    else:
        form=RegisterationForm()
        
    context={
        'form':form
    }
    return render(request,'accounts/register.html',context)



def login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user !=None:
            _transfer_cart_items_to_user(request,user)
            auth.login(request,user)
            messages.success(request,'You are Loged in!')
            # get the previous url from where i came
            url= request.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
                # query-> next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                # params-> {'next': '/cart/checkout/'}
                if 'next' in params:
                    next_page=params['next']
                    return redirect(next_page)
            except:
                return redirect('dashboard')
            
        else:
            messages.error(request,'Invalid Login credentials')
           
    return render(request,'accounts/login.html')

@login_required(login_url="login")
def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context={
        'orders':orders
    }
    return render(request,'accounts/my_order.html',context)


def _transfer_cart_items_to_user(request,user):
    
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        is_cart_item_exists=Cart_Item.objects.filter(cart=cart).exists()
        if is_cart_item_exists:
           _create_or_update_user_cart(request,cart,user)
        else:
            cart_item=Cart_Item.objects.filter(cart=cart)
            for item in cart_item:
                item.user=user
                item.save()
    except:
        pass

def _create_or_update_user_cart(request,cart,user):
    
    cart_item=Cart_Item.objects.filter(cart=cart)
    # get product variation by cart 
    product_variation=[]
    for item in cart_item:
        variation=item.variations.all()
        product_variation.append(list(variation))
    
    # get cart items for logged in user to access his product variation
    cart_item=Cart_Item.objects.filter(user=user)
    ex_var_list=[]
    id=[]
    for item in cart_item:
        existing_variation= item.variations.all()
        ex_var_list.append(list(existing_variation))
        id.append(item.id)
    
    # if product variation found in ex_var_list increase quantity
    for pr in product_variation:
        if pr in ex_var_list:
            index=ex_var_list.index(pr)
            item_id=id[index]
            item=Cart_Item.objects.get(id=item_id)
            item.quantity += 1
            item.user=user
            item.save()
        else:
            cart_item=Cart_Item.objects.filter(cart=cart)
            for item in cart_item:
                item.user=user
                item.save()
                        
                        
                        
@login_required(login_url = "login")
def logout(request):
    auth.logout(request)
    messages.success(request,"You are Logged Out Successfully")
    
    return redirect('login')



@login_required(login_url = "login")
def dashboard(request):
    orders= Order.objects.order_by('created_at').filter(user_id=request.user.id,is_ordered=True)
    order_count=orders.count()
    useprofile=UserProfile.objects.get(user_id=request.user.id)
    context={
        'order_count':order_count,
        'useprofile':useprofile
    }
    return render(request,'accounts/dashboard.html',context)


def activate(request,uidb64,token):
    user =_get_user(uidb64)     
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulations! Your account is activated') 
        return redirect('login')
    
    messages.error(request,'Invalid activation link')
    return redirect('register')


def forgot_password(request):
    if request.method == 'POST':
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
            _change_password_mail(request,user)
            messages.success(request,'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request,'Account does not exists!')
    return render(request,'accounts/forgot_password.html')



def reset_password(request,uidb64,token):
    user=_get_user(uidb64)
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=user.pk
        messages.success(request,'Please reset your password')
        return redirect('reset_password_page')
    
    messages.error(request,'This link has been expired!')
    return redirect('login')

    
def reset_password_page(request):
    if request.method == 'POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password == confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successfully!')
            return redirect('login')
        else:
            messages.error(request,"Passwords do not match!")
            return redirect('reset_password_page')
        
    return render(request,'accounts/reset_password_page.html')



def _create_user(form):
    first_name=form.cleaned_data['first_name']
    last_name=form.cleaned_data['last_name']
    phone_number=form.cleaned_data['phone_number']
    email=form.cleaned_data['email']
    password=form.cleaned_data['password']

    username=email.split("@")[0]
    user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
    user.phone_number=phone_number
    user.save()
    return user

def _add_user_profile_data(user):
    profile = UserProfile()
    profile.user_id = user.id
    profile.profile_picture = 'default/default-user.jpg'
    profile.save()

def _get_user(uidb64):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user= None
    return user




# def _send_user_activation_mail(request,user):
#     current_site=get_current_site(request)
#     mail_subject='Please activate your account'
#     message= render_to_string('mails/account_verification_email.html',{
#         'user':user,
#         'domain':current_site,
#         'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#         'token':default_token_generator.make_token(user),
#     })
#     to_email=user.email
#     send_email=EmailMessage(mail_subject,message,to=[to_email])
#     send_email.send()
    
    
    
    
def _change_password_mail(request,user):
    current_site=get_current_site(request)
    mail_subject='Please reset your password'
    message= render_to_string('mails/reset_password.html',{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
    })
    to_email=user.email
    send_email=EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()