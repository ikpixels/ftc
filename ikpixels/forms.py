from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import PymtCode,MusicorEventPayment



class SubscriptionUploadForm(forms.ModelForm):
    class Meta:
        model= MusicorEventPayment
        fields=['category','payment_method','amount','PaymentReferenceNumber','name','phone']