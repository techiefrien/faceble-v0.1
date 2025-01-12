from django.shortcuts import render ,redirect
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.utils import generate_unique_token
from .utils import date_difference , compress_image
from django.urls import reverse
from django.conf import settings
from payments.models import * 
# Create your views here.


@login_required
def add_events(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        banner = request.FILES.get("banner")
        held_on = request.POST.get('date')
        plan_id = request.POST.get("plan")
        category = request.POST.get("category")

        planObj = pricingFeatures.objects.get(id = plan_id)
        
        if request.user.profile.balance >= planObj.price:
            categoryObj = Event_Categories.objects.get(categoy_name = category)
            
            print(planObj , categoryObj)

            Events.objects.create(
                user = request.user , 
                event_name = name , 
                event_banner = banner , 
                event_category = categoryObj , 
                plan = planObj , 
                held_on =  held_on,
                upload_limit = planObj.upload_limit , 
                selfie_limit = planObj.selfie_limit , 
                ai_matches = planObj.ai_matches , 
                photo_selection_limit  = planObj.photo_selection_limit , 
                event_key = generate_unique_token(8)
                            
            )

            categoryObj.created_count+=1
            categoryObj.save()

            message = f"Purchased new event {name}"
            
            messages.success(request , 'Event Created Successfully !')
            
            PaymentHistory.objects.create(
                user = request.user , 
                message = message  , 
                amount  = planObj.price  , 
                payment_type = 'd' , 
                trans_id=generate_unique_token(6) 
            )
            return redirect(request.path_info)
        else:
            messages.warning(request , "Insufficent Balance In Wallet")
            return redirect(request.path_info)


    event_categories = Event_Categories.objects.all()
    plans = pricingFeatures.objects.filter(plan = request.user.profile.plan)
    return render(request , 'events/add-event.html' , {'event_category':event_categories , 'plans':plans})


def plan_details(request):
    if request.method== 'POST':
        plan_id = request.POST.get("plan_id")
        pricingObj = pricingFeatures.objects.get(id = plan_id)
        context = {
            "upload_limit" : pricingObj.upload_limit,  
            'selfie_limit' : pricingObj.selfie_limit , 
            'ai_match' : pricingObj.ai_matches ,
            'photo_selection' : pricingObj.photo_selection , 
            'photo_selection_limit' : pricingObj.photo_selection_limit , 
            'analytical _report' : pricingObj.analytics_report , 
            'support' : pricingObj.support  , 
            'e_album' : pricingObj.e_album

        }     

        return JsonResponse(context)

    context = {
        "this url only accpets post resuest" : "yes" ,  
    }

    return JsonResponse(context)



def all_events(request):
    return render(request , 'events/all_events.html')

def view_info(request , key):
    eventObj = Events.objects.get(event_key = key)
    date_validity = date_difference( eventObj.created_at , eventObj.plan.valid_date)
    event_categories = Event_Categories.objects.all()

    context =  {
        
        'event':eventObj , 
        'date_validity':date_validity , 
        'event_category':event_categories
        
    }

    return render(request , 'events/view-info.html' , context)


def edit_event_info(request , id):
    
    if request.method == 'POST':
        eventObj = Events.objects.get(id = id)
        name = request.POST.get("name")
        banner = request.FILES.get("banner")
        held_on = request.POST.get('date')
        category = request.POST.get("category")

        categoryObj = Event_Categories.objects.get(categoy_name = category)
        
        eventObj.event_name = name 
        eventObj.event_category = categoryObj
        eventObj.held_on = held_on
        eventObj.event_banner = banner
        eventObj.save()
        messages.success(request , "Event Details Updated successfully !")
        return redirect(reverse('view-info' , args=[eventObj.event_key]))
    return redirect("all-events")



def upload_photos(request , key):
    # Get the event object based on the provided event_key
    eventObj = Events.objects.get(event_key=key)
    
    if request.method == 'POST':
        # Use getlist('images') to fetch all the uploaded files
        if 'images' in request.FILES:
            images = request.FILES.getlist('images')  # List of uploaded files
            print(images)  # Print to verify the files
            
           
            for image in images:
                if eventObj.upload_limit > Photos.objects.filter(event = eventObj).count():
                    compressed_images = compress_image(image)

                    Photos.objects.create(event = eventObj , photo=compressed_images)

                else:
                     return JsonResponse(
                        {
                            'message':'Upload Limit over ! please use add on plan' , 
                            'tags' : 'warning'
                        }
                    )         
           
            return JsonResponse(
                {
                    'message':'Images Uploaded Successfully' , 
                    'tags' : 'success'
                }
            )
        
        else:
            # If no images are selected, display a warning message
            return JsonResponse(
                {
                    'message':'Please select the images to upload' , 
                    'tags' : 'warning'
                }
            )

    # Render the page with the event object if the request is GET or after a POST request
    return render(request, 'events/upload-photos.html', {'event': eventObj})



def photo_gallery(request , key):
    eventObj = Events.objects.get(event_key=key)
    return render(request , 'events/photo-gallery.html' , {'event':eventObj})


def qr_code(request , key):
    eventObj = Events.objects.get(event_key=key)
    custom_url =settings.SITE_DOMAIN+reverse("guest:upload-selfie" , args=[eventObj.event_key])
    return render(request , 'events/qr-code.html' , {'event':eventObj , 'url':custom_url})
