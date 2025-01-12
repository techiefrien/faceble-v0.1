from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def upload_selfie(request ,key):
    
    return  render(request , 'guest/upload-selfie.html')