from django.db import models
from django.contrib.auth.models import User
from events.models import * 

# Create your models here.
class PaymentHistory(models.Model):
    pay_type = [
        ("d" , 'Debit') , 
        ("c" , 'Credit') , 
    ]

    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="payment_history")
    trans_id = models.CharField(max_length=100 , default=None , null=True , blank=True)
    amount = models.FloatField(default=0.0)
    payment_type = models.CharField(max_length=20 , choices=pay_type)
    message = models.CharField(max_length=100)
    date_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user)
    

    class Meta:
        ordering = ['-date_on']
    

class Invoice(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="invoices")
    invoice_id = models.CharField(max_length=10 , unique=True)
    plan_name = models.CharField(max_length=100)
    date_on = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()

    def __str__(self):
        return self.invoice_id
    
    class Meta:
        ordering = ['-date_on']