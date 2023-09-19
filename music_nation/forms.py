from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Album, Song, Customer,Podcasts,Card_Payment,Album_comments


from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField


class PaymentForm(forms.Form):
    cc_number = CardNumberField(label='Card Number')
    cc_expiry = CardExpiryField(label='Expiration Date')
    cc_code = SecurityCodeField(label='CVV/CVC')


class PodcastForm(forms.ModelForm):
    class Meta:
        model= Podcasts
        fields=['title','youtubelink','category']


class AlbumMessageForm(forms.ModelForm):
    class Meta:
        model= Album_comments
        fields=['body',]


class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['address','mobile',
                'account_type','fb','tweeter',
                'instagram','background',
                'fullBiography','profile_pic']     

class NewAlbum(forms.ModelForm):

    class Meta:
        model = Album
        fields = ('album_name','album_genre','album_logo','sell','price')

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required='True')
    first_name = forms.CharField(required='True')
    last_name = forms.CharField(required='True')

    class meta:
        model = User
        fields = (
        'first_name',
        'last_name',
        'email',
        'username',
        'password1',
        'password2',
        )

    def save(self, commit='True'):
        user = super(SignUpForm, self).save(commit='False')
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']


        if commit:
            user.save()
        return user

class NewSong(forms.ModelForm):

    class Meta:
        model = Song
        fields = ('song_name','song_file','Artist','year','sell','price','song_genre',)
