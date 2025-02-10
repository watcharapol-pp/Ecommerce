from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),

    # email verify
    path('email-verify/<str:uidb64>/<str:token>/', views.email_verify, name='email_verify'),

    path('email-verify-sent', views.email_verify_sent, name='email_verify_sent'),

    path('email-verify-fail', views.email_verify_fail, name='email_verify_fail'),
    
    path('email-verify-success', views.email_verify_success, name='email_verify_success'),

    #auth function user login,logout

    path('my-login', views.my_login, name='my_login'),

    path('user-logout', views.user_logout, name='user_logout'),

    #dashboard urls function

    path('dashboard', views.dashboard, name='dashboard'),

    path('profile-manage', views.profile_manage, name='profile_manage'),

    path('delete-acc', views.delete_acc, name='delete_acc'),

    # manage shipping function
    path('manage-shipping', views.manage_shipping, name='manage_shipping'),





]
