from django.urls import path 
from . import views

urlpatterns = [
    path('sign-up/' , views.sign_up , name="sign-up") , 
    path('sign-up/<str:token>/' , views.sign_up , name="sign-up") , 
    path("sign-in/" , views.sign_in , name="sign-in") , 
    path('activate-email/<str:token>/' , views.activate_email , name="activate-email") , 
    path('sign-out/' , views.sign_out , name="sign-out") , 
    path("activate-email-manually/" , views.activate_email_manually , name="activate-email-manually") , 
    path('user-profile' , views.user_profile , name="user-profile") , 
    path('change-profile-image/<str:id>/' , views.change_profile_image ,name="change-profile-image") , 
]