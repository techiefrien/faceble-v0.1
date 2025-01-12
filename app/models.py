from django.db import models

# Create your models here.
class PricingPlans(models.Model):
    plan_name = models.CharField(max_length=100 , unique=True)
    pricing = models.IntegerField(default=0.0)
    is_premium = models.BooleanField(default=False)
    yearly_princing = models.IntegerField(default=0.0 , blank=True , null=True)
    website_access = models.BooleanField(default=False)
    descriptino = models.TextField(null=True , blank=True)

    def __str__(self):
        return self.plan_name


class PlanFeatures(models.Model):
    plan = models.ForeignKey(PricingPlans , on_delete=models.CASCADE , related_name="features")
    is_available = models.BooleanField(default=False)
    feature_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.plan) + "Plan ---> " + self.feature_name


class pricingFeatures(models.Model):

    support_choice = [
        ('chat' , "Chat Support") ,
        ('call' , 'Call Support') , 
        ('remote' , 'Call + Anydesk')
    ]

    plan = models.ForeignKey(PricingPlans , on_delete=models.CASCADE , related_name="plans")
    price = models.FloatField(default=0.0)
    upload_limit = models.IntegerField(default=0)
    selfie_limit = models.IntegerField(default=0)
    ai_matches = models.IntegerField(default=0)
    photo_selection = models.BooleanField(default=False)
    photo_selection_limit = models.IntegerField(default=0)
    analytics_report = models.BooleanField(default=False)
    support = models.CharField(max_length=100 , choices=support_choice)
    e_album = models.BooleanField(default=False)
    valid_date = models.IntegerField(default=30 , help_text="In Days")
    
    

    def __str__(self):
        return str(self.plan)
    

    