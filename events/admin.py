from django.contrib import admin
from .models import * 

# Register your models here.
admin.site.register(Event_Categories)


class photosAdmin(admin.StackedInline):
    model = Photos

class event_admin(admin.ModelAdmin):
    inlines = [photosAdmin]

admin.site.register(Events , event_admin)