from django.db import models
from events.models import Events


# Create your models here.
class Guest(models.Model):
    event = models.ForeignKey(Events , on_delete=models.CASCADE , related_name="guest")
    selfie = models.ImageField(upload_to="selfie/" , null=False , blank=False)
    name = models.CharField(max_length=100 , null=True ,blank=True)
    phone = models.CharField(max_length=10 ,   null=True ,blank=True)
    email = models.EmailField( max_length=255 , null=True ,blank=True)
    send_email = models.BooleanField(default=False)
    send_phone = models.BooleanField(default=False)

    def __str__(self):
        return str(self.event)+" "+self.name