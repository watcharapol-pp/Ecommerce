from django.urls import path
from . import views

urlpatterns = [
    path('payment-process/', views.payment_process, name='payment_process'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    path('payment-fail/', views.payment_fail, name='payment_fail'),
    path('checkout/', views.checkout, name='checkout'),
    path('complete-order/', views.complete_order, name='complete_order'),
]