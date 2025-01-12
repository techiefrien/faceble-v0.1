from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User 
from app.models import PricingPlans
from .models import *
from .utils import *
from django.urls import reverse
from django.contrib.auth import login ,logout , authenticate
from django.contrib.auth.decorators import login_required



# Create your views here.
def sign_up(request , token=None):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method =='POST':
        shop_name = request.POST.get("shop_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        coupon = request.POST.get("coupon")
        
        if User.objects.filter(username = email).exists():
            messages.warning(request , 'Email id already tekane !')
            return redirect(request.path_info)
        elif len(password) < 8:
            messages.warning(request , 'Your Password length should must be atleast 8 characters')
            return redirect(request.path_info)
        else:
            if not coupon:
                create_new_user_object(email = email , shop_name= shop_name , password = password)
                messages.success(request , f'Verfication email sent to {email}')
                return redirect(request.path_info)
            else:
                print(coupon)
                couponobj = coupon_user = Refferel_tokens.objects.filter(token = coupon)
                if not couponobj.exists():
                    messages.warning(request ,f"coupon ({coupon}) does not exists ! please re-check it ")
                    return redirect(request.path_info)
                else:
                    user = create_new_user_object(email = email , shop_name= shop_name , password = password)
                    Refferel_data.objects.create(reffered_by = couponobj[0].assinged_to ,  reffered_to = user)
                    messages.success(request , f'Verfication email sent to {email}')
                    return redirect(request.path_info)
    return render(request , 'accounts/sign_up.html' , {'token':token , "content":"MD01"})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get('password')

        if not User.objects.filter(username = email).exclude():
            messages.warning(request , "Invalid Email Address")
            return redirect(request.path_info)
        
        user = authenticate(username = email , password = password)
        if user is None:
            messages.warning(request , "Invalid Password")
            return redirect(request.path_info)
        else:
            if user.profile.is_verifyed:
                login(request , user)
                messages.success(request , 'Logges In successfully')
                return redirect('home')
            messages.warning(request , "Activate your email to login ")
            return redirect(request.path_info)

    return render(request , 'accounts/sign_in.html')



def activate_email(request , token):
   try:
        profileobj = profile.objects.get(email_token = token)
        profileobj.is_verifyed = True
        profileobj.save()
        messages.success(request , 'Email verifyed successfully')
        return redirect("sign-in")
   except Exception as e:
       return HttpResponse("<h1>Link Expired Please activate account page  !")
   
@login_required
def sign_out(request):
    logout(request)
    messages.info(request , "Login Again")
    return redirect("sign-in")


def activate_email_manually(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        user =  User.objects.filter(username = email)        
        if not user.exists():
            messages.warning(request , 'Email ID is not verifyed')
            return redirect(request.path_info)
        else:
            if user[0].profile.is_verifyed:
                messages.info(request , 'Email id already verifyed')
                return redirect(request.path_info)
            else:
                send_html_email(user[0].username , user[0].first_name , user[0].profile.email_token)
                print(user[0].email , user[0].first_name , user[0].profile.email_token)
                print('email sent')
                messages.info(request , 'Verification email sent successfully !')
                return redirect(request.path_info)
    return render(request , 'accounts/activate_email.html')


@login_required
def user_profile(request):
    return render(request , 'accounts/profile.html')

@login_required
def change_profile_image(request ,id):
    if request.method == 'POST':
        logo = request.FILES.get("logo")

        user = User.objects.get(id = id)
        user.profile.logo = logo 
        user.profile.save()

        return redirect(request.path_info)
    return redirect("user-profile")