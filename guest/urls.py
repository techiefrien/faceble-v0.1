from django.urls import path 
from . import views

app_name = 'guest' 

urlpatterns = [
    path('upload-selfie/<str:key>/' , views.upload_selfie , name='upload-selfie' )
]