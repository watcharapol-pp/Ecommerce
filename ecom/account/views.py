# from email.message import EmailMessage

from django.shortcuts import redirect
from django.template.response import TemplateResponse as render
from django.contrib.auth import update_session_auth_hash
from .forms import CreateUserForm, LoginForm, PasswordUpdateForm, UpdateUserForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from . token import user_tokenizer_generate


from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode 

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def register(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            #email verify setup(template)

            current_site = get_current_site(request)
            subject = 'Verify Your Email'
            message = render_to_string('account/registration/email-verify.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),
                })
            # email = EmailMessage(subject, message, to=[user.email])
            # email.content_subtype = "html"  # ✅ รองรับ HTML Email
            # email.send()



            user.email_user(subject=subject, message=message)
            return redirect('email_verify_sent')
        

            # render_to_string(
            #     'account/registration/email-verify.html',
            #     {'message': message},
            #     request=request
            # )


            # form.save()
            # return redirect('store')


    context = {'form': form}
    return render(request, 'account/registration/register.html', context=context)


def email_verify(request, uidb64, token):
    
    # uniqueid
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)
    
    # Success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email_verify_success')


    # Failed
    else:
        return redirect('email_verify_fail')


def email_verify_sent(request):
    return render(request, 'account/registration/email-verify-sent.html')
    
    # if request.method == 'POST':
    #     email = request.POST.get('email')
    #     user = User.objects.get(email=email)
    #     user.is_active = True
    #     user.save()
    #     return redirect('store')

def email_verify_fail(request):
    return render(request, 'account/registration/email-verify-fail.html')
    

def email_verify_success(request):
    return render(request, 'account/registration/email-verify-success.html')

def my_login(request):
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)

            if user is not None :
                auth.login(request, user)
                return redirect("dashboard")
        
    context = {'form': form}

    return render(request, 'account/my-login.html', context=context)

# Logout
def user_logout(request):
    try:
        for key in list(request.session.keys()):
            if key == 'session_key':
                continue
            else:
                del request.session[key]
    except KeyError:
        pass
    messages.success(request, "Logout success")
    
    return redirect('store')



# dashboard
@login_required(login_url='my_login')
def dashboard(request):
    return render(request, 'account/dashboard.html')

@login_required(login_url='my_login')
def profile_manage(request):
    user = request.user

    # user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        
        user_form = UpdateUserForm(request.POST, instance=user)
        password_form = PasswordUpdateForm(request.POST)
        
        
        if request.POST.get('username') is not None and request.POST.get('new_password') is not None:
            
            user_form.save()
            new_password = request.POST.get('new_password')
            if new_password:
                user.set_password(new_password)
                user.save()
                messages.info(request, "updated success")
                update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
            return redirect('dashboard')
    else:
        user_form = UpdateUserForm(instance=user)
        password_form = PasswordUpdateForm(user)

    # if request.method == 'POST':
    #     user_form = UpdateUserForm(request.POST, instance=request.user)
    #     if user_form.is_valid():
    #         user = user_form.save(commit=False)
    #         new_password = user_form.cleaned_data.get('password1')
    #         if new_password:
    #             user.set_password(new_password)
    #         user_form.save()
    #         return redirect('dashboard')

    #     else:
    #         initial_data = {'password1': user.password}
    #         user_form = UpdateUserForm(instance=user, initial=initial_data)


    context = {
        'user_form': user_form,   
        'password_form': password_form,   
    }
    
    return render(request, 'account/profile-manage.html', context=context )


    # update user and email
    # if request.method == 'POST':
    #     user_form = UpdateUserForm(request.POST, instance=request.user)
    #     email = UpdateUserForm(request.POST, instance=request.user)
    #     password = UpdateUserForm(request.POST, instance=request.user)
    #     # email = request.POST.get('email')
    #     # password = request.POST.get('password')
    #     if user_form.is_valid():
    #         user_form.save()
    #         return redirect('dashboard')
    #     if email.is_valid():
    #         email.save()
    #         return redirect('dashboard')
    #     if password.is_valid():
    #         password.save()
    #         return redirect('dashboard')

    #     # user = request.user
    #     # user.user_form = user_form
    #     # user.email = email
    #     # user.set_password(password)
    #     # user.save()
    #     # return redirect('dashboard')
    #     user_form = UpdateUserForm(request.POST, instance=request.user)
    #     email = UpdateUserForm(request.POST, instance=request.user)
    #     password = UpdateUserForm(request.POST, instance=request.user)
    
    # context = {
    #     'user_form': user_form,
    #     'email': email,
    #     'password': password,
    # }


    
    # return render(request, 'account/profile-manage.html', context=context)

@login_required(login_url='my_login')
def delete_acc(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        messages.error(request, "Acc deleted")
        return redirect('dashboard')
    return render(request, 'account/delete-acc.html', )

# Shipping view
@login_required(login_url='my_login')
def manage_shipping(request):
    try:
        shipping = ShippingAddress.objects.get(user=request.user.id)
        print(shipping)
    except ShippingAddress.DoesNotExist:
        shipping = None 
    form = ShippingForm(instance=shipping)
    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=shipping)
        if form.is_valid():
            # assign user fk on the object
            shipping_user = form.save(commit=False)

            #เพิ่มfkด้วยตัวเอง
            shipping_user.user = request.user
            shipping_user.save()
            messages.info(request, "manage shipping success")
            return redirect('dashboard')
    context = {
            'form': form
        }
    return render(request, 'account/manage-shipping.html', context=context)

