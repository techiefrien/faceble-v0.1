from django.db import models
from django.contrib.auth.models import User
from app.models import *
# Create your models here.
class Event_Categories(models.Model):
    categoy_name = models.CharField(max_length=100 , unique=True)
    created_count = models.IntegerField(default=0)
    default_credits = models.IntegerField(default=150 , null=True , blank=True)

    def __str__(self):
        return self.categoy_name


class Events(models.Model):

    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="events")
    event_name = models.CharField(max_length=100)
    event_banner = models.ImageField(upload_to='event_banners/' , null=True ,blank=True)
    event_key = models.CharField(max_length=100)
    event_category = models.ForeignKey(Event_Categories , on_delete=models.CASCADE  , related_name="events")
    held_on = models.DateField(auto_now_add=True)
    plan = models.ForeignKey(pricingFeatures , on_delete=models.CASCADE , related_name="events")
    upload_limit = models.IntegerField(default=0)
    selfie_limit = models.IntegerField(default=0)
    ai_matches = models.IntegerField(default=0)
    ai_matches_limit = models.IntegerField(default=0)
    photo_selection_limit = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True) 
    created_at = models.DateField(auto_now_add=True)
    


    def __str__(self):
        return str(self.event_name)
    
    class Meta:
        ordering = ['created_at']
    





class Photos(models.Model):
    event = models.ForeignKey(Events , on_delete=models.CASCADE , related_name="photos") 
    photo = models.ImageField(upload_to="event_uploads/")

    def __str__(self):
        return str(self.event)
    
    

