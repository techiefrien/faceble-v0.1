from django.urls import path 
from . import views

urlpatterns = [
    path("add-event/" , views.add_events , name="add-event") ,
    path('plan-details/' , views.plan_details , name="plan-details") , 
    path("all-events" , views.all_events , name="all-events") , 
    path('view-info/<str:key>/' , views.view_info , name='view-info') , 
    path('edit-event-info/<str:id>/' , views.edit_event_info , name="edit-event-info") , 
    path('upload-photos/<str:key>/' , views.upload_photos , name="upload-photos") , 
    path("photo-gallery/<str:key>/" , views.photo_gallery , name="photo-gallery") , 
    path('qr-code/<str:key>/' , views.qr_code , name="qr-code") , 
]