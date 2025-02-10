from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from django import forms




# registration form
class CreateUserForm(UserCreationForm) :
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    # email validation
    
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)


        # make email as required
        self.fields['email'].required = True

        # ป้องกันการใช้อีเมลซ้ำ ในบรรทัดนี้

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Email already exists")
        
        # len function update ###
        if len(email) >= 350:
            raise forms.ValidationError("Email is too long")
        return email
    

    # login form
    
class LoginForm(AuthenticationForm):
        username = forms.CharField(widget=TextInput(
            # attrs={'autofocus': True, 'class': 'username'}
            ))
        password = forms.CharField(widget=PasswordInput(
            # attrs={'class': 'password'}
            ))
        

    # update form USER
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    # password1 = forms.CharField(widget=PasswordInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Password'
    # }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    # passwowrd = None
    # first_name = forms.CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'First Name'
    # }))
    # last_name = forms.CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Last Name'
    # }))

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)


        # make email as required
        self.fields['email'].required = True


    class Meta:
        model = User
        fields = ['username', 'email',]
        # exclude = ['password1', 'password1']

class PasswordUpdateForm(PasswordChangeForm):
    new_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New Password'
    }))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm New Password'
    }))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("The two passwords do not match.")
        
        return cleaned_data
        
