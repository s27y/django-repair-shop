from django import forms

from .models import Address

class RepairQuotationForm(forms.Form):
    customer_name = forms.CharField(max_length=100,
            widget=forms.TextInput(attrs={'class':'form-control'}))
    contact_number = forms.CharField(max_length=100,
            widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'example@gmail.com','class':'form-control'}))
    problem = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    product = forms.CharField(max_length=100,
            widget=forms.TextInput(attrs={'class':'form-control'}))
    serial_number = forms.CharField(max_length=100,
            widget=forms.TextInput(attrs={'class':'form-control'}))

class AddressForm(forms.ModelForm):
    #choice_of_address = forms.ChoiceField()
    
    class Meta:
        model = Address
        exclude = ['user']


