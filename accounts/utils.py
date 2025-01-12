from django.contrib.auth.models import User
from .models import *
from app.models import PricingPlans
from django.conf import settings
from django.urls import  reverse
import random
import string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from accounts.models import Refferel_tokens


def create_new_user_object(email , shop_name , password , **kwargs):
    user = User.objects.create(username = email , first_name = shop_name)
    user.set_password(password)
    user.save()
    pricingObj = PricingPlans.objects.get(plan_name = "Trial Plan")
    token = generate_unique_token() 
    profile.objects.create(user = user , shop_name = shop_name , plan=pricingObj , email_token = token)
    Refferel_tokens.objects.create(token = generate_unique_token(6).upper() , assinged_to = user)
    send_html_email(email , shop_name , token)
    return user 


def generate_unique_token(length=32):
    """Generate a unique alphanumeric token."""
    characters = string.ascii_letters + string.digits  
    token = ''.join(random.choices(characters, k=length))
    return token


def send_html_email(email , shop_name , token):
    subject = "Verify Your Email Address with Faceble"
    recipient_email = email 
    
    link = settings.SITE_DOMAIN+reverse("activate-email" , args=[token]) 

    html_content = render_to_string('email_template.html' , {"shop_name":shop_name , "link":link})
    print(link)
    send_mail(
        subject=subject,
        message='link',  
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient_email],
        html_message=html_content, 
    )
    print("email snet from utils")




