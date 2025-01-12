from django.db import models
from django.contrib.auth.models import User
from app.models import *

# Create your models here.

class profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="profile")
    logo = models.ImageField(upload_to="logos/" , null=True , blank=True)
    shop_name = models.CharField(max_length=100 , null=True , blank=True)
    phone = models.CharField(max_length=10 , null=True , blank=True)
    district = models.CharField(max_length=100  , null=True , blank=True)
    address = models.TextField(max_length=1000 , null=True , blank=True)
    pin_code = models.CharField(max_length=6 ,null=True , blank=True)
    is_verifyed = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100 , null=True , blank=True)
    balance = models.IntegerField(default=0)
    plan = models.ForeignKey(PricingPlans , on_delete=models.CASCADE , related_name="users")
    refferel_points = models.IntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True , null=True , blank=True)  


    def __str__(self):
        return str(self.user)      



class Refferel_tokens(models.Model):
    token = models.CharField(max_length=100 , unique=True)
    assinged_to = models.OneToOneField(User , on_delete=models.CASCADE , related_name="referrel_token")
    refferel_points = models.IntegerField(default=150)

    def __str__(self):
        return str(self.assinged_to) + " " + self.token


class Refferel_data(models.Model):
    reffered_by = models.ForeignKey(User , on_delete=models.CASCADE , related_name="reffered_by")
    reffered_to = models.ForeignKey(User , on_delete=models.CASCADE , related_name="reffered_to")

    def __str__(self):
        return str(self.reffered_by) + " " + str(self.reffered_to)




