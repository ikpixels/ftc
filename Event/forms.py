from . models import Ticket
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class EventForm(forms.ModelForm):
    class Meta:
        model=Ticket
        fields=['ticketCategory','name','district','venue','ticket',
                'regular_price','vip_price','from_t','to_t','from_d','to_d',
                'number_of_tickets','simple_discription',
                'description','youtube_video_link',
                'product_image']



class EventForm2(forms.ModelForm):
    class Meta:
        model=Ticket
        fields=['product_image']


