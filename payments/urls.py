from django.urls import path 
from . import views

urlpatterns = [
    path(f"add-balance/" , views.add_balance , name="add-balance") ,     
    path("payment-history/" , views.view_payment_history , name="payment-history") , 
    path("prcing-plans/" , views.view_plans , name="pricing-plans") , 
    path('upgrade-plan/<str:plan_id>/' , views.upgrade_plan , name="upgrade-plan" ) , 
    path('refer-people/', views.refer_people , name="refer-people") , 
    path('referral-history/' , views.referral_history , name="referral-history") , 
    path('invoice-list/' , views.invoice_list , name='invoice-list') , 
    path('view-invoicd/<str:id>/' , views.view_invoice , name="view-invoice") , 
]