import os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from ftc.settings import MEDIA_ROOT

from ckeditor.fields import RichTextField
from  embed_video.fields  import  EmbedVideoField

from cloudinary.models import CloudinaryField


from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

class Card_Payment(models.Model):
    cc_number = CardNumberField('card number')
    cc_expiry = CardExpiryField('expiration date')
    cc_code = SecurityCodeField('security code')


DISTRICT = (('Balaka','Balaka'),
            ('Blantyre','Blantyre'),
            ('Chikwawa','Chikwawa'),
            ('Chiradzuru','Chiradzuru'),
            ('Chitipa','Chitipa'),
            ('Dedza','Dedza'),
            ('Dowa','Dowa'),
            ('Karonga','Karonga'),
            ('Kasungu','Kasungu'),
            ('Likoma','Likoma'),
            ('Lilongwe','Lilongwe'),
            ('Machinga','Machinga'),
            ('Mangochi','Mangochi'),
            ('Mchinji','Mchinji'),
            ('Mulanje','Mulanje'),
            ('Mwanza','Mwanza'),
            ('Mzimba','Mzimba'),
            ('Neno','Neno'),
            ('Nkhata_Bay','Nkhata_Bay'),
            ('Nkhotakota','Nkhotakota'),
            ('Nsanje','Nsanje'),
            ('Ntcheu','Ntcheu'),
            ('Ntchisi','Ntchisi'),
            ('Phalombe','Phalombe'),
            ('Ruphi','Ruphi'),
            ('Salima','Salima'),
            ('Thyolo','Thyolo'),
            ('Zomba','Zomba'),
            ('Others','Others')
            )


GENRE = ( ('House','House'),
          ('Hip Hop','Hip hop'), 
          ('Trap','Trap'),
          ('Raggie','Raggie'),
          ('Amapiano','Amapiano'),
          ('Gospel','Gospel'),
          ('Beats','Beats'),
          ('Afro pop','Afro pop'),
          ('Afro House','Afro House'),
          ('Dancehall','Dancehall'),
          ('Poetry','Poetry/Poem'),
          ('Rock','Rock'),
          ('Blues','Blues'),
          ('Classical','Classical'),
          ('Country','Country'),
          ('Electronic','Electronic'),
          ('Indie','Indie'),
          ('Jazz','Jazz'),
          ('Latino','Latino'),
          ('R&B','R&B'),
        )
 

USER_CAT = (
    ('Artist','Artist'),
    )

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    account_type = models.CharField(max_length=40,choices=USER_CAT)
    #profile_pic = models.ImageField(upload_to='image',null=True,blank=True)
    profile_pic= CloudinaryField('profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    artist_genre = models.CharField(max_length=30,choices=GENRE)
    fb = models.URLField(null=True,blank=True)
    tweeter = models.URLField(null=True,blank=True)
    instagram = models.URLField(null=True,blank=True)
    background = models.CharField(max_length=200,null=True,blank=True)
    fullBiography = RichTextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name

def user_directory_path(self, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(self.album_artist.id, filename)

def user_directory_path_song(self, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>

    return 'user_{0}/{1}'.format(self.song_album.album_artist.id, filename)

FREE_OR_NOT =(
      ('Free','Free'),
      ('Sale','Sale'),
    )

# Create your models here.
class Album(models.Model):
    album_name = models.CharField(max_length=30)
    uploaded_on = models.DateTimeField(auto_now=True)
    album_logo = CloudinaryField('artwork',null=True,blank=True)
    album_genre = models.CharField(max_length=30,choices=GENRE)
    aboutAlbum = RichTextField(null=True,blank=True)
    songsNum = models.PositiveIntegerField(default=0)
    streamNum = models.PositiveIntegerField(default=0)
    sell  = models.CharField(choices=FREE_OR_NOT,max_length=100)
    most_sold = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=18, decimal_places=2,default=0.00)
    album_artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.album_name

    def artist(self):
        user = self.album_artist
        artist = Customer.objects.get(user=user).id
        return artist


class Album_comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    album = models.ForeignKey(Album,on_delete=models.CASCADE, related_name='msg')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'msg'



class Song(models.Model):
    song_name = models.CharField(max_length=40)
    Artist = models.CharField(max_length=40,null=True,blank=True)
    song_album = models.ForeignKey(Album,on_delete=models.CASCADE, related_name='songs')
    song_file = CloudinaryField('song',unique_filename=False,use_filename =True,null=True,blank=True,folder="ikpixels.com/music",resource_type="video",)
    song_genre = models.CharField(max_length=30,choices=GENRE)
    video = EmbedVideoField(null=True,blank=True)
    streamingCount = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField(default=0)
    sell  = models.CharField(choices=FREE_OR_NOT,max_length=100)
    most_sold = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=18, decimal_places=2,default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.song_name +' '+ str(self.song_album)

    def song_logo(self):
        return self.song_album.album_logo

    def album(self):
        return self.song_album

PodCategory = (
      ('Music','Music'),
      ('Arts','Arts'),
      ('Business','Business'),
      ('Comedy','Comedy'),
      ('Education','Education'),
      ('Fiction','Fiction'),
      ('Government','Government'),
      ('History','History'),
      ('Health & Fitness','Health & Fitness'),
      ('Kids & Family','Kids & Family'),
      ('Leisure','Leisure'),
      ('News','News'),
      ('Religion & Spirituality','Religion & Spirituality'),
      ('Science','Science'),
      ('Society & Culture','Society & Culture'),
      ('Sports','Sports'),
      ('Technology','Technology'),
      ('True Crime','True Crime'),
      ('TV & Film','TV & Film'),
    )


class Podcasts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='podcast')
    title = models.CharField(max_length=40)
    category = models.CharField(max_length=40,choices = PodCategory,default="Music")
    youtubelink = EmbedVideoField(null=True,blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def split_link(self):
        link = self.youtubelink
        youtube,Id = link.split('?v=')
        final_link = "https://www.youtube.com/embed/" + Id
        return final_link

class contacts(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    email = models.CharField(max_length=100,blank=True,null=True)
    subject = models.CharField(max_length=100,blank=True,null=True)
    body = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name