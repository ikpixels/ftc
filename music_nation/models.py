import os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.utils.text import slugify
from django.dispatch import receiver

from ftc.settings import MEDIA_ROOT

from ckeditor.fields import RichTextField
from  embed_video.fields  import  EmbedVideoField

from cloudinary.models import CloudinaryField


from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

class Card_Payment(models.Model):
    cc_number = CardNumberField('card number')
    cc_expiry = CardExpiryField('expiration date')
    cc_code = SecurityCodeField('security code')


def upload_audio_location(instance,filename):
    basename,extension =filename.split('.mp3')
    return "%s/%s_%s_%s_%s.%s"%( 'Audio','www.ikpixels.com',instance.song_name,'by',instance.Artist,'.mp3')

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
    profile_pic= models.ImageField(upload_to='profile/%y/%m/%d',null=True,blank=True,default="ikartwork.jpg")
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    artist_genre = models.CharField(max_length=30,choices=GENRE)
    fb = models.URLField(null=True,blank=True)
    tweeter = models.URLField(null=True,blank=True)
    instagram = models.URLField(null=True,blank=True)
    background = models.CharField(max_length=200,null=True,blank=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
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
    @property
    def image_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url

    def get_absolute2_url(self):
        return reverse('music_nation_views:ArtistDetail',kwargs ={'slug':self.slug})


def create_user_slug(instance,new_slug=None):

    slug = slugify(str(instance.user))
    if new_slug is not None:
        slug = new_slug

    qs = Customer.objects.filter(slug=slug).order_by('-id')

    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug,qs.first().id)
        return create_user_slug(instance,new_slug=new_slug)
    return slug

def pre_save_receiver_user(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_user_slug(instance)
pre_save.connect(pre_save_receiver_user,sender=Customer)





def user_directory_path(self, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(self.album_artist.id, filename)

def user_directory_path_song(self, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>

    return 'user_{0}/{1}'.format(self.song_album.album_artist.id, filename)

FREE_OR_NOT =(
      ('Free','Free'),
      #('Sale','Sale'),
    )


class AlbumObjectManager(models.Manager):
    def get_queryset(self):
        album = super(AlbumObjectManager, self).get_queryset().filter( aproved=True)
        return album


class AdminAlbumObjectManager(models.Manager):
    def get_queryset(self):
        songs = super(AdminAlbumObjectManager, self).get_queryset().filter(aproved=False)
        return songs

class ArtistAlbumObjectManager(models.Manager):
    def get_queryset(self):
        album = super(ArtistAlbumObjectManager, self).get_queryset().all()
        return album

# Create your models here.
class Album(models.Model):
    album_name = models.CharField(max_length=30)
    uploaded_on = models.DateTimeField(auto_now=True)
    album_logo = models.ImageField(upload_to='artwork/%y/%m/%d',null=True,blank=True,default="ikartwork.jpg")
    #album_logo = CloudinaryField('artwork',null=True,blank=True)
    album_genre = models.CharField(max_length=30,choices=GENRE)
    aboutAlbum = RichTextField(null=True,blank=True)
    songsNum = models.PositiveIntegerField(default=0)
    streamNum = models.PositiveIntegerField(default=0)
    sell  = models.CharField(choices=FREE_OR_NOT,max_length=100)
    most_sold = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True,null=True,blank=True)
    price = models.DecimalField(max_digits=18, decimal_places=2,default=0.00)
    album_artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    aproved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AlbumObjectManager()
    AdminAlbumAproval = AdminAlbumObjectManager()
    artistObjects = ArtistAlbumObjectManager()

    def __str__(self):
        return self.album_name
    @property
    def artist(self):
        user = self.album_artist
        artist = Customer.objects.get(user=user).slug
        return artist
    @property
    def image_url(self):
        if self.album_logo and hasattr(self.album_logo, 'url'):
            return self.album_logo

    def get_absolute_url(self):
        return reverse('music_nation_views:album_detail',kwargs ={'slug':self.slug})

    def delete_media(self):
        os.remove(path=MEDIA_ROOT+'/'+str(self.album_logo))

def create_album_slug(instance,new_slug=None):

    name = str(instance.album_name) + " by " + str(instance.album_artist)

    slug = slugify(name)
    if new_slug is not None:
        slug = new_slug

    qs = Album.objects.filter(slug=slug).order_by('-id')

    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug,qs.first().id)
        return create_album_slug(instance,new_slug=new_slug)
    return slug

def pre_save_receiver_album(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_album_slug(instance)
pre_save.connect(pre_save_receiver_album,sender=Album)


class Album_comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    album = models.ForeignKey(Album,on_delete=models.CASCADE, related_name='msg')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'msg'


class SongObjectManager(models.Manager):
    def get_queryset(self):
        songs = super(SongObjectManager, self).get_queryset().filter(aproved=True)
        return songs

class AdminSongObjectManager(models.Manager):
    def get_queryset(self):
        songs = super(AdminSongObjectManager, self).get_queryset().filter(aproved=False)
        return songs

class ArtistSongObjectManager(models.Manager):
    def get_queryset(self):
        songs = super(ArtistSongObjectManager, self).get_queryset().all()
        return songs


class Song(models.Model):
    song_name = models.CharField(max_length=40)
    Artist = models.CharField(max_length=40,null=True,blank=True)
    song_album = models.ForeignKey(Album,on_delete=models.CASCADE, related_name='songs')
    song_file=models.FileField(upload_to=upload_audio_location,null=True,blank=True)
    artwork = models.ImageField(upload_to='artwork/%y/%m/%d',null=True,blank=True,default="ikartwork.jpg")
    song_genre = models.CharField(max_length=30,choices=GENRE)
    video = EmbedVideoField(null=True,blank=True)
    streamingCount = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField(default=0)
    sell  = models.CharField(choices=FREE_OR_NOT,max_length=100)
    most_sold = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=18, decimal_places=2,default=0.00)
    aproved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SongObjectManager()
    adminAprove = AdminSongObjectManager()
    ArtistSongObject  = ArtistSongObjectManager()

    def __str__(self):
        return self.song_name +' '+ str(self.song_album)

    def song_logo(self):
        return self.song_album.album_logo

    def album(self):
        return self.song_album

    def delete_media(self):
        os.remove(path=MEDIA_ROOT+'/'+str(self.song_file))

    def artst_url(self):
        album = Album.objects.get(id=self.song_album.id).album_artist
        artist_slug = Customer.objects.get(user=album).slug
        return artist_slug

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