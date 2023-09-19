from django import forms
from django.contrib.auth.models import User
from . import models



class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        
"""class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['address','mobile','profile_pic']"""

class ProductForm(forms.ModelForm):
    class Meta:
        model=models.Product
        fields=['name','price','simple_discription','description',
        'product_image','product_image2',
        'product_image3','product_image4','category','youtube_video_link']

#address of shipment
class AddressForm(forms.ModelForm):
    class Meta:
        model=models.Orders
        fields=['email','mobile','payment_method','address','acc_Name','refu']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model=models.Feedback
        fields=['name','feedback']

#for updating status of order
class OrderForm(forms.ModelForm):
    class Meta:
        model=models.Orders
        fields=['status']

#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
