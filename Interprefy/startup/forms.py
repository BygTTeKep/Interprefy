from typing import Any
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
import re
from .models import (
    CUser,
    Products
    
)


# def validate_phone_number(phonenumber):
#     if re.search(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$',phonenumber) == None:
#         raise ValidationError(
#             _("неверный формат номера телефона")
#         )

# def validate_fullname(fullname:str):
#     if len(fullname.split()) != 3:
#         raise ValidationError(
#             _("%(value)s ")# <================================
#         )
    # И если есть другие знаки кроме букв

# def validName(name):
#     if Intermediares.objects.filter(Name=name).exists():
#         return ValidationError(_("name already exists"))

class IntermediaresForm(forms.ModelForm):
    # Name = forms.CharField(max_length=50, validators=[validName])
    Email = forms.EmailField(widget=forms.EmailInput(attrs={"type":"email", 'class':'form-control', 'placeholder':'example@example.com'}))
    Description = forms.CharField(widget=forms.Textarea(attrs={"rows":"5",'class':'form-control'}))
    class Meta:
        model = CUser
        fields = ('username', 'Email', 'Description')



class ClientForm(UserCreationForm):
    TelephoneNumber = forms.CharField(max_length=15,required=True,widget=forms.TextInput(attrs={'type': 'tel', 
                                                                                                'class':"form-control", 
                                                                                                "placeholder":"+7 (987)654-32-10",
                                                                                                }))
    FullName = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'class':"form-control", 
                                                                                           "placeholder":"Имя Фамилия Отчество", 
                                                                                           "id":"FullName",
                                                                                           "pattern": "",
                                                                                           }))
    # pin = forms.IntegerField(required=True,min_value=10**5, max_value=10**6)
    class Meta:
        model = CUser
        fields = 'username', 'FullName', 'TelephoneNumber', "password1", "password2"
    


    def __init__(self, *args, **kwargs):
        # pattern для FullName и для TelephoneNumber
        
        super(ClientForm, self).__init__(*args, **kwargs)    
        self.fields['TelephoneNumber'].widget.attrs['id'] = 'TelephoneNumber'
        self.fields['TelephoneNumber'].widget.attrs['pattern'] = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'   
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('Name', 'Price', 'UnitsInStock', 'ImageProducts')
    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.fields['ImageProducts'].required = False


# class ReviewsForm(forms.ModelForm):
#     # Подумать над прикреплением картинки
#     class Meta:
#         model = Reviews
#         fields = ('Review','Image')