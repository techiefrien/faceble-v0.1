from django.shortcuts import render , redirect
from django.contrib import messages
from .models import *
import datetime
from accounts.utils import generate_unique_token 
from django.urls import reverse
from django.conf import settings
# Create your views here.
def add_balance(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        request.user.profile.balance += int(amount)
        request.user.profile.save()
        payment_msg = f"Recharged for Rupees {float(amount)}"
        print(payment_msg)
        PaymentHistory.objects.create(user = request.user , amount = amount , payment_type = "c" , trans_id=generate_unique_token(6) , message = payment_msg)
        messages.success(request , 'Payment Added Successfully')
        return redirect(request.path_info)
    return render(request , 'payments/wallet.html')


def view_payment_history(request):
    paymentobjs = PaymentHistory(user = request.user)
    return render(request , 'payments/payment-history.html')


def view_plans(request):
    plansObjs = PricingPlans.objects.all()
    return render(request , "payments/plans.html" , {'plans':plansObjs})


def upgrade_plan(request , plan_id):
    planObj = PricingPlans.objects.get(id = plan_id)
    if request.user.profile.plan.plan_name == "Trial Plan":
        has_refferel = request.user.reffered_to.exists()
        if has_refferel:
            refferd_by = request.user.reffered_to.first().reffered_by
            ref_points = refferd_by.referrel_token.refferel_points
            refferd_by.profile.balance = ref_points
            PaymentHistory.objects.create(
                                            user = refferd_by, 
                                            amount = ref_points , 
                                            payment_type = "c" , 
                                            trans_id=generate_unique_token(6) , 
                                            message = f"Referrel Bonus {ref_points} for {request.user.username}'s joining"
                                        )
            refferd_by.profile.balance += ref_points
            refferd_by.profile.save()
            refferd_by.profile.save()
            request.user.profile.plan = planObj
            request.user.profile.save()
            Invoice.objects.create(user = request.user , invoice_id = generate_unique_token(5).upper , plan_name = planObj.plan_name  , amount=planObj.pricing)
            messages.success(request , 'Plan upgraded successfully!')
            return redirect("home")
            
        else:
            request.user.profile.plan = planObj
            request.user.profile.save()
            Invoice.objects.create(user = request.user , invoice_id = generate_unique_token(5).upper() , plan_name = planObj.plan_name  , amount=planObj.pricing)
            messages.success(request , 'Plan upgraded successfully!')
            return redirect("home")
            
    else:
        request.user.profile.plan = planObj
        request.user.profile.save()
        Invoice.objects.create(user = request.user , invoice_id = generate_unique_token(5).upper() , plan_name = planObj.plan_name  , amount=planObj.pricing)    
        messages.success(request , 'Plan upgraded successfully!')
        return redirect("home")

    return redirect('home')


def refer_people(request):
    referrel_link = settings.SITE_DOMAIN + reverse('sign-up' , args=[request.user.referrel_token.token])
    referral_count = request.user.reffered_by.filter(reffered_to__profile__plan__plan_name = 'Trial Plan').count()
    total_ref_count = request.user.reffered_by.all().count()
    print('total ref count : ' , total_ref_count)
    print('purchasers : ' , referral_count)
    return render(request , 'payments/refer-people.html' , {'ref_link':referrel_link , 'ref_count':total_ref_count-referral_count , "total_ref_count":total_ref_count})


def referral_history(request):
    return render(request , 'payments/referral-history.html')


def invoice_list(request):
    return render(request , 'payments/invoice-list.html')

def view_invoice(requets ,id):
    invoiceObj = Invoice.objects.get(invoice_id = id)
    return render(requets , 'payments/invoice.html' , {'invoice':invoiceObj})