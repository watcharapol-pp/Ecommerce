from django import forms
from .models import ShippingAddress
class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'email', 'address1','address2', 'city', 'state', 'zipcode', ]
        exclude = ['user',]

#     card_number = forms.CharField(max_length=16, required=True, widget=forms.TextInput(attrs={'placeholder': 'Card Number'}))
#     card_expiry = forms.CharField(max_length=5, required=True, widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
#     card_cvc = forms.CharField(max_length=3, required=True, widget=forms.TextInput(attrs={'placeholder': 'CVC'}))
#     cardholder_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Cardholder Name'}))